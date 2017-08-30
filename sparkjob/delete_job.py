import sys
from pyspark.sql import SparkSession


def delete_df_job(name):
    spark = SparkSession.builder.appName(name).enableHiveSupport().getOrCreate()
    spark.sql('DROP TABLE IF EXISTS ' + name + ' PURGE')

if __name__ == '__main__':
    name = sys.argv[1]
    delete_df_job(name)
