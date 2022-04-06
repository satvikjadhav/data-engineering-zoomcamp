#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types


# In[2]:


spark = SparkSession.builder.master("local[*]").appName('test').getOrCreate()


# In[4]:


get_ipython().system('wget https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_2021-01.csv')


# In[5]:


get_ipython().system('wc -l fhvhv_tripdata_2021-01.csv')


# In[6]:


df = spark.read.option("header", "true").csv('fhvhv_tripdata_2021-01.csv')


# In[7]:


df.show()


# In[9]:


# getting the first 101 rows
get_ipython().system('head -n 101 fhvhv_tripdata_2021-01.csv > head.csv')


# In[10]:


get_ipython().system('head -n 10 head.csv')


# In[12]:


dfp = pd.read_csv('head.csv')


# In[13]:


dfp.dtypes


# In[16]:


# now we use this information to create a spark dataframe
spark.createDataFrame(dfp).schema


# In[3]:


schema = types.StructType([
    types.StructField('hvfhs_license_num', types.StringType(), True),
    types.StructField('dispatching_base_num', types.StringType(), True),
    types.StructField('pickup_datetime', types.TimestampType(), True),
    types.StructField('dropoff_datetime', types.TimestampType(), True),
    types.StructField('PULocationID', types.IntegerType(), True),
    types.StructField('DOLocationID', types.IntegerType(), True),
    types.StructField('SR_Flag', types.StringType(), True)
])


# In[4]:


df = spark.read.option("header", "true").schema(schema).csv('fhvhv_tripdata_2021-01.csv')


# In[5]:


df.head(10)


# In[23]:





# In[7]:


df.write.parquet('fhvhv/2021/01/')


# In[6]:


# Spark DataFrame video


# In[8]:


df = spark.read.parquet('fhvhv/2021/01/')


# In[10]:


df.printSchema()


# In[11]:


# Now, what can we do with this dataframe


# In[12]:


# selecting individual columns
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'PULocationID')


# In[15]:


# for filtering data
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'PULocationID').filter(df.hvfhs_license_num == 'HV0003').show()


# In[16]:


# Using spark functions
from pyspark.sql import functions as F


# In[17]:


# F.to_date()
df.withColumn('pickup_date', F.to_date(df.pickup_datetime)) .withColumn('dropoff_datet', F.to_date(df.dropoff_datetime))     .show()


# In[18]:


# Creating our functions
def crazy_stuff(base_num):
    num = int(base_num[1:])
    if num % 7 == 0:
        return f's/{num:03x}'
    elif num % 3 == 0:
        return f'a/{num:03x}'
    else:
        return f'e/{num:03x}'


# In[19]:


crazy_stuff('B02884')


# In[20]:


crazy_stuff_udf = F.udf(crazy_stuff, returnType=types.StringType())


# In[21]:


d.withColumn('pickup_date', F.to_date(df.pickup_datetime)).withColumn('dropoff_datet', F.to_date(df.dropoff_datetime)).withColumn('base_id', crazy_stuff_udf(df.dispatching_base_num)).show()


# In[ ]:




