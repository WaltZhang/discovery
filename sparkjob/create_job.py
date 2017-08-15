import json, sys, uuid

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


def create_df_job(name, path, schema):
    spark = SparkSession.builder.appName(name).getOrCreate()
    fields = []
    text = json.loads(schema)
    print(text)
    for title in text:
        type = switcher.get(title.get('type'))
        if type is None:
            type = title.get('type')
        field = StructField(title.get('name'), type())
        fields.append(field)
    df = spark.read.csv(path, schema=StructType(fields))
    df.printSchema()
    df.show()
    df.write.saveAsTable(name)
    # df.write.parquet(os.path.join(settings.DATA_WAREHOUSE_HOME, name))


def persist_df(df, format='parquet'):
    table_name = uuid.uuid1()
    df.withColumn(uuid, )
    df.write.saveAsTable(table_name, format=format)


if __name__ == '__main__':
    name = sys.argv[1]
    path = sys.argv[2]
    schema = sys.argv[3]
    print(name)
    print(path)
    print(schema)
    create_df_job(name, path, schema)
