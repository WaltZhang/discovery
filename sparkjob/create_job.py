import json
import sys

import requests
from pyspark.sql import SparkSession
from pyspark.sql.types import *

switcher = {
    'null': NullType,
    'bool': BooleanType,
    'byte': ByteType,
    'short': ShortType,
    'integer': IntegerType,
    'long': LongType,
    'float': FloatType,
    'double': DoubleType,
    'date': DateType,
    'timestamp': TimestampType,
    'string': StringType,
}


class SparkJob:
    def save(self):
        raise NotImplementedError()


class SparkManager(object):
    @classmethod
    def factory(cls, source_type, *args):
        class CsvJob(SparkJob):
            def __init__(self, *args):
                self.name = args[0]
                self.path = args[1]
                self.schema_path = args[2]

            def save(self):
                spark = SparkSession.builder.appName(self.name).enableHiveSupport().getOrCreate()
                fields = []
                schema = self.schema.replace('\'', '\"')
                cols = json.loads(schema)
                for col in cols:
                    col_type = switcher.get(col.get('type'))
                    if col_type is None:
                        col_type = col.get('type')
                    field = StructField(col.get('name'), col_type())
                    fields.append(field)
                df = spark.read.csv(self.path, schema=StructType(fields), header=True)
                df.printSchema()
                df.show()
                df.write.saveAsTable(self.name)
                spark.sql('select count(*) from ' + self.name).show()

        class JdbcJob(SparkJob):
            def __init__(self, *args):
                self.name = args[0]
                self.connector_id = args[1]
                self.table = args[2]

            def save(self):
                connector = self.get_connector()
                jdbc_url = "jdbc:mysql://{0}:{1}/{2}".format(connector.get('host'), connector.get('port'), connector.get('db'))
                spark = SparkSession.builder.appName(self.name).enableHiveSupport().getOrCreate()


            def get_connector(self):
                url = "http://localhost:8080/connectors/api/" + self.connector_id
                response = requests.get(url)
                return json.loads(response.text)

        job_types = {"csv": CsvJob, "jdbc": JdbcJob}

        if source_type in job_types:
            return job_types[source_type](*args)
        return None


if __name__ == "__main__":
    source = sys.argv[1]
    args = sys.argv[2:]
    job = SparkManager.factory(source, *args)
    job.save() if job is not None else print(source)
