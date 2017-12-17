import json
import sys
import requests
from pyspark.sql import SparkSession

from discovery import utils


def query_data(name):
    spark = SparkSession.builder.appName(name).enableHiveSupport().getOrCreate()
    return spark.sql('SELECT * FROM {}'.format(name))


def create_sample(df):
    rdd = df.toJSON()
    sample = []
    for e in rdd.take(1000):
        sample.append(json.loads(e))
    return sample


def format_schema(dtypes):
    schema_list = []
    for dtype in dtypes:
        schema = {}
        schema[dtype[0]] = dtype[1]
        schema_list.append(schema)
    return schema_list


def create_inventory(name):
    df = query_data(name)
    sample_data = create_sample(df)
    schema = format_schema(df.dtypes)
    schema_string = json.dumps(schema)
    sample_string = json.dumps(sample_data)
    context = {
        "name": name,
        "schema": schema_string,
        "sample": sample_string
    }
    url = utils.get_service_url('inventory')
    requests.post(url, json=context)


if __name__ == '__main__':
    name = sys.argv[1]
    create_inventory(name)
