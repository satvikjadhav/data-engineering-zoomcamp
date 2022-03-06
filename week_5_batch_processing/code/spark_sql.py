#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.master("local[*]").appName('test').getOrCreate()


# In[17]:


df_green = spark.read.parquet('data/pq/green/*')


# In[18]:


df_yellow = spark.read.parquet('data/pq/yellow/*')


# In[19]:


df_yellow.columns


# In[20]:


# getting the common columns between the two dataframes


# In[21]:


set(df_green.columns) & set(df_yellow.columns)


# In[22]:


df_green = df_green.withColumnRenamed('lpep_pickup_datetime', 'pickup_datetime').withColumnRenamed('lpep_dropoff_datetime', 'dropoff_datetime')


# In[23]:


df_yellow = df_yellow.withColumnRenamed('tpep_pickup_datetime', 'pickup_datetime').withColumnRenamed('tpep_dropoff_datetime', 'dropoff_datetime')


# In[24]:


common_colums = []

yellow_columns = set(df_yellow.columns)

for col in df_green.columns:
    if col in yellow_columns:
        common_colums.append(col)

common_colums


# In[25]:


# we use the .lit to create a column with a literal value; in this case the color of the taxi
df_green_sel = df_green.select(common_colums).withColumn('service_type', F.lit('green'))


# In[26]:


df_yellow_sel = df_yellow.select(common_colums).withColumn('service_type', F.lit('yellow'))


# In[27]:


# now we union the two dataframes into one dataframe which will be our 'trips_all' data
df_trips_data = df_green_sel.unionAll(df_yellow_sel)


# In[29]:


df_trips_data.groupBy('service_type').count().show()


# In[30]:


# Using sql in Spark to query the above dataframe


# In[31]:


# Tell spark that the dataframe in question is a table. And only then can we use queries on it


# In[32]:


df_trips_data.registerTempTable('trips_data')


# In[33]:


spark.sql("""
SELECT
    service_type,
    count(1)
FROM
    trips_data
GROUP BY 
    service_type
""").show()


# In[34]:


df_result = spark.sql("""
SELECT 
    -- Reveneue grouping 
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month, 
    service_type, 

    -- Revenue calculation 
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,
    SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
    AVG(passenger_count) AS avg_montly_passenger_count,
    AVG(trip_distance) AS avg_montly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3
""")


# In[35]:


df_result.show(n=20)


# In[38]:


df_test = spark.sql("""
select revenue_zone, revenue_monthly_fare, avg_montly_passenger_count, avg_montly_trip_distance from

(SELECT 
    -- Reveneue grouping 
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month, 
    service_type, 

    -- Revenue calculation 
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,
    SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
    AVG(passenger_count) AS avg_montly_passenger_count,
    AVG(trip_distance) AS avg_montly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3) as table_a
""")


# In[39]:


df_test.show(n=20)


# In[41]:


# to write our output as a parquet file
# If we don't add coalesce, we would get multiple small parquet files 
# Coalesce function is the same as repartition, except we want to use it when we want to reduce the number of partitions
df_result.coalesce(1).write.parquet('data/report/revenue/', mode='overwrite')


# In[ ]:




