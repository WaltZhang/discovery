import json
import sys
import requests
from pyspark.sql import SparkSession


def query_schema_job(name):
    spark = SparkSession.builder.appName(name).enableHiveSupport().getOrCreate()
    df = spark.sql('SELECT * FROM {}'.format(name))
    return df.dtypes


def format_schema(dtypes):
    schema = {}
    for dtype in dtypes:
        schema[dtype[0]] = dtype[1]
    return schema


def create_inventory(name):
    dtypes = query_schema_job(name)
    schema = format_schema(dtypes)
    string = json.dumps(schema).replace('\'', '\"')
    print(type(schema), string)
    url = 'http://localhost:8080/inventory/api/'
    context = {
        "name": name,
        "schema": string
    }
    requests.post(url, json=context)


if __name__ == '__main__':
    name = sys.argv[1]
    print(name)
    create_inventory(name)
