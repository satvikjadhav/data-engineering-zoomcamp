# Introduction to Spark

## What is Apache Spark 
- Apache Spark is an open-source unified analytics engine for large-scale data processing. Spark provides an interface for programming clusters with implicit data parallelism and fault tolerance
- Apache Spark is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters

- A data processing **Engine**

- Sample Process:
	- Take data from our data Lake
	- Load data to the machines on which spark is being run on
	- Then output the data to a data lake or a data warehouse

- Distributed
	- Can have multiple machines working together to process the same data
	- Makes it faster

- Can be used for Batch jobs and Streaming

## When to use Spark?

- Typically used when our data is in a data lake
	- Parquet files are preferred

### Typical Workflow using Spark
1. Raw data to a data lake
2. Add transformations or joins on this data using Presto or Athena (SQL based) - most of Pre processing here
3. Spark doing intensive tasks on this data (which cannot be done via SQL)
	- Using spark, we can take the trained model in python and use spark to apply the model
4. Python - Training/ML
5. Result can go to a Data Lake or a Data Warehouse

**Spark comes in handy when we want to deal with data only in the datalake.** 
- For example, we want to take some data from the datalake, process it, run some transformations on it, and then put it back in datalake
- In this case, we didn't touch the data warehouse at all

As a result, we are able to utilize data warehouse for doing analytics, and keep it separate from data processing and related activities


## First Look at Spark/Pyspark

SparkSession is the object that we use to interact with Spark

```python
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
```

## Reading CSV Files

Unlike `Pandas`, `Spark` doesn't try to infer the data type

A simple work around for this is by using Pandas to infer the data types, and then creating our schema using this information
- In spark, each `Integer` takes 4 bytes and each `Long` takes 8 bytes worth of data

To create a spark dataframe from a csv file:
```python
df = spark.read \
    .option("header", "true") \
    .csv('fhvhv_tripdata_2021-01.csv')
```

using the `schema` on our spark dataframe, we can get the schema output such as:
```scala
StructType(List(StructField(hvfhs_license_num,StringType,true),StructField(dispatching_base_num,StringType,true),StructField(pickup_datetime,StringType,true),StructField(dropoff_datetime,StringType,true),StructField(PULocationID,LongType,true),StructField(DOLocationID,LongType,true),StructField(SR_Flag,DoubleType,true)))
```

`StructType` is something that comes from `Scala`, but we need to turn this into a python code

We will use this to declare a schema for our dataframe

And we transform it to as follows:
```python
schema = types.StructType([
    types.StructField('hvfhs_license_num', types.StringType(), True),
    types.StructField('dispatching_base_num', types.StringType(), True),
    types.StructField('pickup_datetime', types.TimestampType(), True),
    types.StructField('dropoff_datetime', types.TimestampType(), True),
    types.StructField('PULocationID', types.IntegerType(), True),
    types.StructField('DOLocationID', types.IntegerType(), True),
    types.StructField('SR_Flag', types.StringType(), True)
])
```

Note: The other way to infer the schema (apart from pandas) for the csv files, is to set the `inferSchema` option to `true` while reading the files in Spark

And now when we read in a csv file, we can use the schema variable as follows:
```python
df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv('fhvhv_tripdata_2021-01.csv')
```

## Partitions

Since our csv file a one large file, only one spark executer will take care of it, and this is not efficient

To overcome this, we can `partition` our file into multiple smaller files which can then be used by the idle spark executers, thus making it more efficient

We can think of a partition as roughly a separate file

We can do this by using the following command: 
```python
df = df.repartition(24)
```

Repartitioning is quite an expensive operation 

And then to save this file as a parquet: 
```python
df.write.parquet('fhvhv/2021/01/')
```
