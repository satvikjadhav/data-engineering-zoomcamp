import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

credentials_location = '/home/satvikjadhav/.google/credentials/google_credentials.json'

# Creating spark config
conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "./lib/gcs-connector-hadoop3-2.2.5.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)

# We will first make the spark context then make the spark session
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

# This is essentially saying that when we see a file system that starts with GS, we need to use the implementation
# coming from the JAR file used to connect to google cloud storage, and use the google cloud credentials
hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

df_yellow = spark.read.parquet('gs://dtc_data_lake_data-engineering-339113/pq/yellow/taxi_data/*')

df_yellow.count()