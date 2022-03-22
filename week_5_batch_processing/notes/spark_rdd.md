# Spark Resilient Distributed Dataset (RDD)

## Operations on Spark RDDs: Map and Reduce

Going to be expressing the following SQL query in RDD terms:
```sql
SELECT 
    date_trunc('hour', tpep_pickup_datetime) AS hour, 
    PULocationID AS zone,

    SUM(total_amount) AS amount,
    COUNT(1) AS number_records
FROM
    yellow
WHERE
    tpep_pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2
```

### What is RDD and how is it related to DataFrames

DataFrames are built on top of RDDs.
Before DataFrames, RDDs were used. 
DataFrame gives us a nice API and functions so we don't need to actually use RDDs. 
DataFrames have a schema
RDDs are a collection of objects

A DataFrame has a field called `rdd` which can be accessed as follows: `df_green.rdd`
- This is the internal or underlying RDD of the DataFrame in question

The DataFrame that we have is actually built on top of RDD of rows
- Row is a special object that is used in building DataFrames

If we want to keep only select columns we can do the following: 
```python
rdd = df_green \
    .select('lpep_pickup_datetime', 'PULocationID', 'total_amount') \
    .rdd
```

### Operations on RDDs: map, filter, reduceByKey

`map` is applied to every element in a RDD, but 'filter' only returns `true` or `false`

`map` takes in an object, in our case `Row`, and outputs something else
- It applies some transformation to every element in the RDD and outputs some other RDD

reduce by key
- Input is a RDD (key, value) in the reduce by key function
- output is a RDD (key, reduced-value)
- Takes a group of elements with multiple similar Keys.
- It will reduce all the keys into one key. Similar to Group By in SQL

How this looks is as follows in our context:
```python
def calculate_revenue(left_value, right_value):
    left_amount, left_count = left_value
    right_amount, right_count = right_value
    
    output_amount = left_amount + right_amount
    output_count = left_count + right_count
    
    return (output_amount, output_count)
```

For example, we have the following:
``` 
Key1, Value1
Key1, Value2
```
It would then add the two values (Value1, Value2)

```
Value1 + Value2 = ResultValue
```

And our new output would be:
``` 
Key1, ResultValue
```

The reason why we need to do the `reshuffling` is because we have bunch of partitions, and for each partitions we are applying `map` function which turns our records into `key, value` pair. 
And we want to make sure that all the keys in different partitions end up in the same partitions
And for this the `reshuffling` is done

### From DataFrame to RDD

```python
df_result = rdd \
    .filter(filter_outliers) \
    .map(prepare_for_grouping) \
    .reduceByKey(calculate_revenue) \
    .map(unwrap) \
    .toDF(result_schema)
```

### From RDD to DataFrame

```python
import pandas as pd

rows = duration_rdd.take()
df = pd.DataFrame(rows, columns=columns)
```

## Spark RDD mapPartition

What `mapPartition` is doing is the following:
1. Input: RDD Partition - Entire chunk of data
2. Apply some function to this chunk of data
3. Output: New modified RDD Partition that we have applied the function on

This is particularly useful when we have, for example, 1 terabyte of data. 
And since we don't have 1 terabyte of RAM, we would partition this into, say, chunks of 100mb partitions. 
We can now process those chunks separately. 

This is also convenient when we want to use do Machine Learning related tasks.
- For example, applying Machine Learning predictions to a data set. 
- Since we can't load in a 1 terabyte file, we would partition that 1 terabyte file into smaller chunks and apply the Machine Learning model using the `mapPartition` function


