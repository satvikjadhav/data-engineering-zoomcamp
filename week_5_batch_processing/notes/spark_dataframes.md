# Spark DataFrames

Parquet files contain metadata about schema. 
Even if we have multiple parquet files of a CSV file, it wouldn't be a problem

We can use `Spark` almost like `Pandas` as well

If we want to only select specific columns, then:
```python
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'PULocationID')
```

For filtering:
```python
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'PULocationID').filter(df.hvfhs_license_num == 'HV0003')
```

In spark there is a distinction between things being executed right away, and things that are not executed right away

## Actions vs Transformations

**Transformations**
- Not executed right away
- Selecting columns
- Filtering
- Joins
- Group By
- Applying some function to the columns
- Known as Lazy Evaluation


**Actions**
- Executed right away
- Show()
- Take()
- Head()
- Write (the results as csv or parquet)
- The whole "Process" made by spark is evaluated to know the results
- Known as Eager

### Functions already available in spark
- using: `from pyspark.sql import functions as F`
- They let us apply some `function` on a column of a table in order to transform the data in some way
- 


One of the things that Spark gives us are User Defined Functions (UDFs)
- Using `udf` function from `from pyspark.sql import functions as F`
- Turning our custom function into a udf:
	- `crazy_stuff_udf = F.udf(crazy_stuff, returnType=types.StringType())`

