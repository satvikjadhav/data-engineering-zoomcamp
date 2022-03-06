#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyspark
from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql import types
import os


# In[2]:


# Our objective here is to read the csv files and define a shcema for them and then save them in parquet format


# In[3]:


spark = SparkSession.builder.master("local[*]").appName('test').config("spark.executor.memory", "28g").config("spark.driver.memory", "4g").getOrCreate()

#     .config(“spark.sql.files.maxPartitionBytes”, 1024 * 1024 * 128) \
#     .config("spark.executor.memory", "16g") \
#     .config("spark.driver.memory", "28g") \


# In[4]:


print(spark.conf.get("spark.executor.memory"))
print(spark.conf.get("spark.driver.memory"))


# In[11]:


df = spark.read.option("header", "true").csv('data/raw/yellow/2010/yellow_tripdata_2010_01.csv', inferSchema=True)


# In[12]:


df.printSchema()


# In[22]:


# Getting schema info


# In[25]:


dfp = pd.read_csv('data/raw/green/2020/green_tripdata_2020_01.csv', nrows=1000)


# In[27]:


spark.createDataFrame(dfp).schema


# In[4]:


green_schema = types.StructType([
    types.StructField("VendorID", types.IntegerType(), True),
    types.StructField("lpep_pickup_datetime", types.TimestampType(), True),
    types.StructField("lpep_dropoff_datetime", types.TimestampType(), True),
    types.StructField("store_and_fwd_flag", types.StringType(), True),
    types.StructField("RatecodeID", types.IntegerType(), True),
    types.StructField("PULocationID", types.IntegerType(), True),
    types.StructField("DOLocationID", types.IntegerType(), True),
    types.StructField("passenger_count", types.IntegerType(), True),
    types.StructField("trip_distance", types.DoubleType(), True),
    types.StructField("fare_amount", types.DoubleType(), True),
    types.StructField("extra", types.DoubleType(), True),
    types.StructField("mta_tax", types.DoubleType(), True),
    types.StructField("tip_amount", types.DoubleType(), True),
    types.StructField("tolls_amount", types.DoubleType(), True),
    types.StructField("ehail_fee", types.DoubleType(), True),
    types.StructField("improvement_surcharge", types.DoubleType(), True),
    types.StructField("total_amount", types.DoubleType(), True),
    types.StructField("payment_type", types.IntegerType(), True),
    types.StructField("trip_type", types.IntegerType(), True),
    types.StructField("congestion_surcharge", types.DoubleType(), True)
])

yellow_schema = types.StructType([
    types.StructField("VendorID", types.IntegerType(), True),
    types.StructField("tpep_pickup_datetime", types.TimestampType(), True),
    types.StructField("tpep_dropoff_datetime", types.TimestampType(), True),
    types.StructField("passenger_count", types.IntegerType(), True),
    types.StructField("trip_distance", types.DoubleType(), True),
    types.StructField("RatecodeID", types.IntegerType(), True),
    types.StructField("store_and_fwd_flag", types.StringType(), True),
    types.StructField("PULocationID", types.IntegerType(), True),
    types.StructField("DOLocationID", types.IntegerType(), True),
    types.StructField("payment_type", types.IntegerType(), True),
    types.StructField("fare_amount", types.DoubleType(), True),
    types.StructField("extra", types.DoubleType(), True),
    types.StructField("mta_tax", types.DoubleType(), True),
    types.StructField("tip_amount", types.DoubleType(), True),
    types.StructField("tolls_amount", types.DoubleType(), True),
    types.StructField("improvement_surcharge", types.DoubleType(), True),
    types.StructField("total_amount", types.DoubleType(), True),
    types.StructField("congestion_surcharge", types.DoubleType(), True)
])


# In[5]:


yellow_schema_old = types.StructType([
    types.StructField("vendor_name", types.StringType(), True),
    types.StructField("Trip_Pickup_DateTime", types.TimestampType(), True),
    types.StructField("Trip_Dropoff_DateTime", types.TimestampType(), True),
    types.StructField("Passenger_Count", types.IntegerType(), True),
    types.StructField("Trip_Distance", types.DoubleType(), True),
    types.StructField("Start_Lon", types.DoubleType(), True),
    types.StructField("Start_Lat", types.DoubleType(), True),
    types.StructField("Rate_Code", types.StringType(), True),
    types.StructField("store_and_forward", types.StringType(), True),
    types.StructField("End_Lon", types.IntegerType(), True),
    types.StructField("End_Lat", types.DoubleType(), True),
    types.StructField("Payment_Type", types.StringType(), True),
    types.StructField("Fare_Amt", types.DoubleType(), True),
    types.StructField("surcharge", types.DoubleType(), True),
    types.StructField("mta_tax", types.DoubleType(), True),
    types.StructField("Tip_Amt", types.DoubleType(), True),
    types.StructField("Tolls_Amt", types.DoubleType(), True),
    types.StructField("Total_Amt", types.DoubleType(), True)
])


# In[5]:


yellow_schema_old_new = types.StructType([
   types.StructField("vendor_id", types.StringType(), True),
   types.StructField("pickup_datetime", types.TimestampType(), True),
   types.StructField("dropoff_datetime", types.TimestampType(), True),
   types.StructField("passenger_count", types.IntegerType(), True),
   types.StructField("trip_distance", types.DoubleType(), True),
   types.StructField("pickup_longitude", types.DoubleType(), True),
   types.StructField("pickup_latitude", types.DoubleType(), True),
   types.StructField("rate_code", types.StringType(), True),
   types.StructField("store_and_fwd_flag", types.StringType(), True),
   types.StructField("dropoff_longitude", types.IntegerType(), True),
   types.StructField("dropoff_latitude", types.DoubleType(), True),
   types.StructField("payment_type", types.StringType(), True),
   types.StructField("fare_amount", types.DoubleType(), True),
   types.StructField("surcharge", types.DoubleType(), True),
   types.StructField("mta_tax", types.DoubleType(), True),
   types.StructField("tip_amount", types.DoubleType(), True),
   types.StructField("tolls_amount", types.DoubleType(), True),
   types.StructField("total_amount", types.DoubleType(), True)
])


# In[10]:


df = spark.read.option("header", "true").schema(green_schema).csv('data/raw/green/2020/', inferSchema=True)


# In[30]:


df.printSchema()


# In[33]:


# getting list of items in a directory using python
os.listdir('data/raw/green/2020/')


# In[34]:


# for green taxi data
years = [2020, 2021]

for year in years:
    print(f'processing data for {year}')

    input_path = f'data/raw/green/{year}/'
    output_path = f'data/pq/green/{year}/'

    df_green = spark.read.option("header", "true").schema(green_schema).csv(input_path)

    df_green.write.parquet(output_path)


# In[40]:


df = spark.read.option("header", "true").schema(yellow_schema_old).csv('data/raw/yellow/2012/yellow_tripdata_2012_01.csv')


# In[41]:


df.show(5)


# In[14]:


# for older data, preprocessing step
df_yellow = spark.read.option("header", "true").schema(yellow_schema).csv('data/raw/yellow/2009/yellow_tripdata_2009_01.csv')
    
# changing column names
df_yellow.withColumnRenamed("vendor_name","VendorID").withColumnRenamed("Trip_Pickup_DateTime","tpep_pickup_datetime").withColumnRenamed("Trip_Dropoff_DateTime","tpep_dropoff_datetime").withColumnRenamed("Passenger_Count","passenger_count").withColumnRenamed("Trip_Distance","trip_distance").withColumnRenamed("Start_Lon","RatecodeID").withColumnRenamed("Start_Lat","store_and_fwd_flag").withColumnRenamed("Rate_Code","PULocationID").withColumnRenamed("store_and_forward","DOLocationID").withColumnRenamed("End_Lon","payment_type").withColumnRenamed("End_Lat","fare_amount").withColumnRenamed("Payment_Type","extra").withColumnRenamed("Fare_Amt","mta_tax").withColumnRenamed("surcharge","tip_amount").withColumnRenamed("mta_tax","tolls_amount").withColumnRenamed("Tip_Amt","improvement_surcharge").withColumnRenamed("Tolls_Amt","total_amount").withColumnRenamed("Total_Amt","congestion_surcharge") 

df_ye.write.parquet('data/pq/yellow/2009/')


# In[19]:


df_parq = spark.read.parquet('data/pq/yellow/2009/*')
df_parq.printSchema()
df_parq.select(['VendorID']).show(5)


# In[6]:


df_csv = spark.read.csv('data/raw/yellow/2011/yellow_tripdata_2011_01.csv', inferSchema=True)


# In[7]:


df_csv.show(5)


# In[5]:


df = pd.read_csv('data/raw/yellow/2011/yellow_tripdata_2011_01.csv', nrows=100000)

df


# In[9]:


df = pd.read_csv('data/raw/yellow/2014/yellow_tripdata_2014_03.csv', nrows=1000)
df


# In[5]:


os.environ["PYSPARK_SUBMIT_ARGS"] = "--driver-memory 2g"


# In[11]:


# for yellow taxi data
years = [2014]

for year in years:
    print(f'processing data for {year}')

    input_path = f'data/raw/yellow/{year}/'
    output_path = f'data/pq/yellow/{year}/'

    df_yellow = spark.read.option("header", "true").schema(yellow_schema_old_new).csv(input_path)

    df_yellow.write.parquet(output_path)


# In[ ]:




