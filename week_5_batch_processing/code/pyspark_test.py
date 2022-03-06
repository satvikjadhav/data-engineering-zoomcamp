#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyspark


# In[2]:


pyspark.__version__


# In[3]:


pyspark.__file__


# In[4]:


from pyspark.sql import SparkSession


# In[5]:


spark = SparkSession.builder.master("local[*]").appName('test').getOrCreate()


# In[7]:


get_ipython().system('wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv')


# In[10]:


df = spark.read.option("header", "true").csv('taxi+_zone_lookup.csv')


# In[11]:


df.show()


# In[12]:


df.write.parquet('zones')


# In[14]:


get_ipython().system('ls')


# In[ ]:




