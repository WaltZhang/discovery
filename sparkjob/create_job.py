import json
import sys

from pyspark.sql import SparkSession
from pyspark.sql.types import *

from discovery import utils

switcher = {
    'null': NullType,
    'boolean': BooleanType,
    'tinyint': ByteType,
    'smallint': ShortType,
    'int': IntegerType,
    'bigint': LongType,
    'float': FloatType,
    'double': DoubleType,
    'date': DateType,
    'timestamp': TimestampType,
    'string': StringType,
    'decimal': DecimalType,
    'array': ArrayType,
    'map': MapType
}


class SparkJob:
    def save(self):
        raise NotImplementedError()


class SparkManager(object):
    @classmethod
    def factory(cls, source_type, *job_args):
        class CsvJob(SparkJob):
            def __init__(self, *csv_args):
                self.path = csv_args[0]
                self.schema = csv_args[1]
                self.name = csv_args[2]
                self.delimiter = csv_args[3]

            def save(self):
                spark = SparkSession.builder.appName(self.name).enableHiveSupport().getOrCreate()
                fields = []
                cols = json.loads(self.schema)
                for col in cols:
                    for k, v in col.items():
                        col_type = switcher.get(v)
                        if col_type is None:
                            col_type = StringType
                        field = StructField(k, col_type())
                        fields.append(field)
                df = spark.read.csv(self.path, schema=StructType(fields), header=True, sep=self.delimiter)
                df.printSchema()
                df.show()
                df.write.saveAsTable(self.name)
                spark.sql('select count(*) from ' + self.name).show()

        class JdbcJob(SparkJob):
            def __init__(self, *jdbc_args):
                self.connector_id = jdbc_args[0]
                self.table = jdbc_args[1]
                self.name = jdbc_args[2]

            def save(self):
                connector = utils.get_connector()
                jdbc_url = "jdbc:mysql://{0}:{1}/{2}?user={3}&password={4}".format(
                    connector.get('host'),
                    connector.get('port'),
                    connector.get('db'),
                    connector.get('user'),
                    connector.get('password')
                )
                spark = SparkSession.builder.appName(self.name).enableHiveSupport().getOrCreate()
                df = spark.read.jdbc(url=jdbc_url, table=self.table)
                df.write.saveAsTable(self.name)
                spark.sql('select count(*) from ' + self.name).show()

        job_types = {"csv": CsvJob, "jdbc": JdbcJob}

        if source_type in job_types:
            return job_types[source_type](*job_args)
        return None


if __name__ == "__main__":
    source = sys.argv[1]
    args = sys.argv[2:]
    job = SparkManager.factory(source, *args)
    job.save()
