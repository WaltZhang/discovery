import json
import sys

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


def create_df_job(name, path, schema, header):
    spark = SparkSession.builder.appName(name).enableHiveSupport().getOrCreate()
    fields = []
    schema = schema.replace('\'', '"')
    cols = json.loads(schema)
    for col in cols:
        col_type = switcher.get(col.get('type'))
        if col_type is None:
            col_type = col.get('type')
        field = StructField(col.get('name'), col_type())
        fields.append(field)
    df = spark.read.csv(path, schema=StructType(fields), header=header)
    df.printSchema()
    df.show()
    df.write.saveAsTable(name)
    spark.sql('select count(*) from ' + name).show()


if __name__ == '__main__':
    name = sys.argv[1]
    path = sys.argv[2]
    schema = sys.argv[3]
    # header = sys.argv[4] if sys.argv[4] else True
    print(name)
    print(path)
    print(schema)
    create_df_job(name, path, schema, True)
