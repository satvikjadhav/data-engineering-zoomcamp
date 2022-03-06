#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pyspark
from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql import types
import os
from pyspark.sql import functions as F


# In[2]:


spark = SparkSession.builder.master("local[*]").appName('test').config("spark.executor.memory", "28g").config("spark.driver.memory", "4g").getOrCreate()


# In[3]:


# quesiton 1: Whats the spark verion?
spark.version
# Answer: 3.0.3


# In[4]:


# quesiton 2: What's the size of the folder with results (in MB)?
# Downloading file
get_ipython().system('wget https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_2021-02.csv')


# In[5]:


# adding schema
schema = types.StructType([
    types.StructField('hvfhs_license_num', types.StringType(), True),
    types.StructField('dispatching_base_num', types.StringType(), True),
    types.StructField('pickup_datetime', types.TimestampType(), True),
    types.StructField('dropoff_datetime', types.TimestampType(), True),
    types.StructField('PULocationID', types.IntegerType(), True),
    types.StructField('DOLocationID', types.IntegerType(), True),
    types.StructField('SR_Flag', types.StringType(), True)
])


# In[7]:


# creating the df
df = spark.read.option("header", "true").schema(schema).csv('fhvhv_tripdata_2021-02.csv')


# In[10]:


# repartitioning and saving as parquet
df.repartition(24).write.parquet('fhvhv/2021/02/')
# Answer: 208 MB


# In[11]:


# Question 3: count records
df = spark.read.parquet('fhvhv/2021/02/')


# In[12]:


df.show(5)


# In[24]:


count = df.filter(F.to_date(df.pickup_datetime) == '2021-02-15')


# In[29]:


count.count()
# Answer: 367170


# In[45]:


# Question 4. Longest trip
# Calculate Time difference in Seconds
time_calc = df.withColumn("time_delta_seconds", df.dropoff_datetime.cast("long") - df.pickup_datetime.cast("long"))


# In[46]:


# converting the df to a table
time_calc.registerTempTable('time_calc')


# In[50]:


spark.sql("""
SELECT
    hvfhs_license_num, pickup_datetime, dropoff_datetime, time_delta_seconds
FROM
    time_calc
ORDER BY 
    time_delta_seconds DESC
""").show(5)
# Answer: 2021-02-11


# In[52]:


# Question 5: Most frequent dispatching_base_num
df.registerTempTable('fhvfeb')


# In[56]:


spark.sql("""
SELECT
    hvfhs_license_num, count(1) as frequency
FROM
    fhvfeb
GROUP BY
    hvfhs_license_num
ORDER BY frequency desc
""").show()
# Answer: HV0003, 8290758. Stages = 2


# In[63]:


# Question 6. Most common locations pair
# creating zones df and parquet
zones = spark.read.option("header", "true").csv('taxi+_zone_lookup.csv')


# In[65]:


zones.write.parquet('zones')


# In[66]:


zonespq = spark.read.parquet('zones')


# In[68]:


zonespq.registerTempTable('zones')


# In[70]:


df.show(5)
zonespq.show(5)


# In[82]:


spark.sql("""
SELECT
    zones_pu.Zone as zones_pu, zones_du.Zone as zones_pu, count(*) as frequency
FROM 
    fhvfeb AS fhv 
LEFT JOIN 
    zones as zones_pu
ON 
    fhv.PULocationID = zones_pu.LocationID
LEFT JOIN
    zones as zones_du
ON
    fhv.DOLocationID = zones_du.LocationID
GROUP BY
    zones_pu.Zone, zones_du.Zone
ORDER BY 
    frequency DESC
""").show(5)
# Answer: East New York / East New York
