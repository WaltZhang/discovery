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
    text = json.loads(schema)
    print(text)
    for title in text:
        type = switcher.get(title.get('type'))
        if type is None:
            type = title.get('type')
        field = StructField(title.get('name'), type())
        fields.append(field)
    df = spark.read.csv(path, schema=StructType(fields), header=header)
    df.printSchema()
    df.show()
    df.write.saveAsTable(name)
    spark.sql('show tables').show()
    spark.sql('select 1 from ' + name).show()


if __name__ == '__main__':
    name = sys.argv[1]
    path = sys.argv[2]
    schema = sys.argv[3]
    header = sys.argv[4] if sys.argv[4] else True
    print(name)
    print(path)
    print(schema)
    create_df_job(name, path, schema, header)
