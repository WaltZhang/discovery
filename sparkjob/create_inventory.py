import json
import sys
import requests
from pyspark.sql import SparkSession

from discovery import utils


def query_data(name):
    spark = SparkSession.builder.appName(name).enableHiveSupport().getOrCreate()
    return spark.sql('SELECT * FROM {}'.format(name))


def create_sample(df, name):
    if df.count() > 100000:
        df = df.limit(100000)
    df.write.csv("/tmp/" + name)


def format_schema(dtypes):
    schema = {}
    for dtype in dtypes:
        schema[dtype[0]] = dtype[1]
    return schema


def create_inventory(name):
    df = query_data(name)
    create_sample(df, name)
    schema = format_schema(df.dtypes)
    string = json.dumps(schema).replace('\'', '\"')
    url = utils.get_service_url('inventory')
    context = {
        "name": name,
        "schema": string
    }
    requests.post(url, json=context)


if __name__ == '__main__':
    name = sys.argv[1]
    create_inventory(name)
