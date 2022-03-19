# Spark Internals

## Anatomy of a Spark Cluster
	Spark Cluster, Spark Driver, Master, and Executors

In spark, when we set `.master()` to `local[*]`, it creates a `local cluster`

```mermaid
flowchart LR;
    a[/"driver (Spark job)"\]--"spark-submit<br/>port 4040"-->master
    subgraph cluster ["Spark cluster"]
    master(["master"])
    master-->e1{{executor}}
    master-->e2{{executor}}
    master-->e3{{executor}}
    end
    subgraph df ["Dataframe (in S3/GCS)"]
    p0[partition]
    e1<-->p1[partition]:::running
    e2<-->p2[partition]:::running
    e3<-->p3[partition]:::running
    p4[partition]
    style p0 fill:#080
    classDef running fill:#b70;
    end
```

Usually, the way it works is as follows:
1. We create a script in `python` or `scala` with some spark code on our laptop, or in Airflow for example
2. We have an independent Spark cluster.
	- In here we have a computer or a node that we will call `spark master`
	- The role of `spark master` is to coordinate jobs
3. We submit our code to this `spark cluster` and to the `spark master`
	- We use `spark-submit` to sent the package with our code to the master and we specify some information such as: 
		- What are the resources we need to do this job for example
4. In the `spark cluster` we have computers or nodes known as `executors` which do the actual computations
5. Each executor will fetch a dataframe partition stored in a Data Lake (usually S3, GCS or a similar cloud provider), do something with it and then store it somewhere, which could be the same Data Lake or somewhere else. If there are more partitions than executors, executors will keep fetching partitions until every single one has been processed.
6. This is in contrast to Hadoop, another data analytics engine, whose executors locally store the data they process. Partitions in Hadoop are duplicated across several executors for redundancy, in case an executor fails for whatever reason (Hadoop is meant for clusters made of commodity hardware computers). However, data locality has become less important as storage and data transfer costs have dramatically decreased and nowadays it's feasible to separate storage from computation, so Hadoop has fallen out of fashion.
7. Today, since most big data is in the cloud, and the `spark cluster` is also usually in the same data center, so downloading the data required is fast. 
8. The prefered way is to keep the data in S3 or GCS, have a `spark cluster` and then do our big data work that way

There is a `driver`	that submits the code to the `spark master` in a `spark cluster`


## GroupBy in Spark

The query we will be using as an example will be the following: 

```python
df_green_revenue = spark.sql("""
SELECT 
    date_trunc('hour', lpep_pickup_datetime) AS hour, 
    PULocationID AS zone,
    SUM(total_amount) AS amount,
    COUNT(1) AS number_records
FROM
    green
WHERE
    lpep_pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2  
""")
```

This query will output the total revenue and amount of trips per hour per zone. We need to group by hour and zones in order to do this

Since the data is split along partitions, it's likely that we will need to group data which is in separate partitions, but executors only deal with individual partitions. Spark solves this issue by separating the grouping in 2 stages:

1. In the first stage, each executor groups the results in the partition they're working on and outputs the results to a temporary partition. These temporary partitions are the ***intermediate results***.
	* `Executors` in `spark` can only process one partition at a time

```mermaid
graph LR
    subgraph df [dataframe]
    p1[partition 1]
    p2[partition 2]
    p3[partition 3]
    end
    subgraph ex [executors]
    e1{{executor 1}}
    e2{{executor 2}}
    e3{{executor 3}}
    end
    subgraph ir [intermediate group by]
    i1("hour 1, zone 1, 100 revenue, 5 trips<br/>hour 1, zone 2, 200 revenue, 10 trips")
    i2("hour 1, zone 1, 50 revenue, 2 trips<br/>hour 1, zone 2, 250 revenue, 11 trips")
    i3("hour 1, zone 1, 200 revenue, 10 trips<br/>hour 2, zone 1, 75 revenue, 3 trips")
    end
    p1-->e1
    p2-->e2
    p3-->e3
    e1-->i1
    e2-->i2
    e3-->i3
```

2. The second stage ***shuffles*** the data, and in this case is also known as ***reshuffling***: Spark will put all records with the ***same keys*** (in this case, the `GROUP BY` keys which are hour and zone) in the ***same partition***. The algorithm to do this is called _external merge sort_. Once the shuffling has finished, we can once again apply the `GROUP BY` to these new partitions and ***reduce*** the records to the ***final output***.
    * Note that the shuffled partitions may contain more than one key, but all records belonging to a key should end up in the same partition.

```mermaid
graph LR
    subgraph IR [intermediate results]
        i1("hour 1, zone 1, 100 revenue, 5 trips<br/>hour 1, zone 2, 200 revenue, 10 trips")
        i2("hour 1, zone 1, 50 revenue, 2 trips<br/>hour 1, zone 2, 250 revenue, 11 trips")
        i3("hour 1, zone 1, 200 revenue, 10 trips<br/>hour 2, zone 1, 75 revenue, 3 trips")
    end
    subgraph F [shuffling]
        f1("hour 1, zone 1, 100 revenue, 5 trips<br/>hour 1, zone 1, 50 revenue, 2 trips<br/>hour 1, zone 1, 200 revenue, 10 trips")
        f2("hour 1, zone 2, 200 revenue, 10 trips<br/>hour 1, zone 2, 250 revenue, 11 trips<br/>hour 2, zone 1, 75 revenue, 3 trips")
    end
    subgraph R ["reduced records - final group by"]
        r1("hour 1, zone 1, 350 revenue, 17 trips")
        r2("hour 1, zone 2, 450 revenue, 21 trips")
        r3("hour 2, zone 1, 75 revenue, 3 trips")
    end
    i1-->f1 & f2
    i2 --> f1 & f2
    i3 --> f1 & f2
    f1-->r1
    f2-->r2 & r3
```

Running the query should display the following DAG in the Spark UI:

```mermaid
flowchart LR
    subgraph S1 [Stage 1]
        direction TB
        t1(Scan parquet)-->t2("WholeStageCodegen(1)")
        t2 --> t3(Exchange)
    end
    subgraph S2 [Stage 2]
        direction TB
        t4(Exchange) -->t5("WholeStageCodegen(2)")
    end
    t3-->t4
```
* The `Exchange` task refers to the shuffling.

If we were to add sorting to the query (adding a `ORDER BY 1,2` at the end), Spark would perform a very similar operation to `GROUP BY` after grouping the data. The resulting DAG would look liked this:

```mermaid
flowchart LR
    subgraph S1 [Stage 1]
        direction TB
        t1(Scan parquet)-->t2("WholeStageCodegen(1)")
        t2 --> t3(Exchange)
    end
    subgraph S2 [Stage 2]
        direction TB
        t4(Exchange) -->t5("WholeStageCodegen(2)")
    end
    subgraph S3 [Stage 3]
        direction TB
        t6(Exchange) -->t7("WholeStageCodegen(3)")
    end
    t3-->t4
    t5-->t6
```

By default, Spark will repartition the dataframe to 200 partitions after shuffling data. For the kind of data we're dealing with in this example this could be counterproductive because of the small size of each partition/file, but for larger datasets this is fine.

Shuffling is an ***expensive operation***, so it's in our best interest to reduce the amount of data to shuffle when querying.
* Keep in mind that repartitioning also involves shuffling data.


## Joins in Spark

Joining tables in Spark is implemented in a similar way to `GROUP BY` and `ORDER BY`, but there are 2 distinct cases: joining 2 large tables and joining a large table and a small table.

### Joining 2 large tables

Let's assume that we've created a `df_yellow_revenue` dataframe in the same manner as the `df_green_revenue` we created in the previous section. We want to join both tables, so we will create temporary dataframes with changed column names so that we can tell apart data from each original table:

```python
df_green_revenue_tmp = df_green_revenue \
    .withColumnRenamed('amount', 'green_amount') \
    .withColumnRenamed('number_records', 'green_number_records')

df_yellow_revenue_tmp = df_yellow_revenue \
    .withColumnRenamed('amount', 'yellow_amount') \
    .withColumnRenamed('number_records', 'yellow_number_records')
```
* Both of these queries are _transformations_; Spark doesn't actually do anything when we run them.

We will now perform an [outer join](https://dataschool.com/how-to-teach-people-sql/sql-join-types-explained-visually/) so that we can display the amount of trips and revenue per hour per zone for green and yellow taxis at the same time regardless of whether the hour/zone combo had one type of taxi trips or the other:

```python
df_join = df_green_revenue_tmp.join(df_yellow_revenue_tmp, on=['hour', 'zone'], how='outer')
```
* `on=` receives a list of columns by which we will join the tables. This will result in a ***primary composite key*** for the resulting table.
* `how=` specifies the type of `JOIN` to execute.

When we run either `show()` or `write()` on this query, Spark will have to create both the temporary dataframes and the joint final dataframe. The DAG will look like this:

```mermaid
graph LR
    subgraph S1[Stage 1]
        direction TB
        s1(Scan parquet)-->s2("WholeStageCodegen(3)")-->s3(Exchange)
    end
    subgraph S2[Stage 2]
        direction TB
        s4(Scan parquet)-->s5("WholeStageCodegen(1)")-->s6(Exchange)
    end
    subgraph S3[Stage 3]
        direction TB
        s7(Exchange)-->s8("WholeStageCodegen(2)")
        s9(Exchange)-->s10("WholeStageCodegen(4)")
        s8 & s10 -->s11(SortMergeJoin)-->s12("WholeStageCodegen(5)")
    end
    s3-->s9
    s6-->s7
```

Stages 1 and 2 belong to the creation of `df_green_revenue_tmp` and `df_yellow_revenue_tmp`.

For stage 3, given all records for yellow taxis `Y1, Y2, ... , Yn` and for green taxis `G1, G2, ... , Gn` and knowing that the resulting composite key is `key K = (hour H, zone Z)`, we can express the resulting complex records as `(Kn, Yn)` for yellow records and `(Kn, Gn)` for green records. Spark will first ***shuffle*** the data like it did for grouping (using the ***external merge sort algorithm***) and then it will ***reduce*** the records by joining yellow and green data for matching keys to show the final output.

```mermaid
graph LR
    subgraph Y [yellow taxis]
        y1("(K1, Y1)<br/>(K2, Y2)")
        y2("(K3, Y3)")
    end
    subgraph G [green taxis]
        g1("(K2, G1)<br/>(K3, G2)")
        g2("(K4, G3)")
    end
    subgraph S [shuffled partitions]
        s1("(K1, Y1)<br/>(K4, G3)")
        s2("(K2, Y2)<br/>(K2, G1)")
        s3("(K3, Y3)<br/>(K3, G2)")
    end
    subgraph R [reduced partitions]
        r1("(K1, Y1, Ø)<br/>(K4, Ø, G3)")
        r2("(K2, Y2, G1)")
        r3("(K3, Y3, G2)")
    end
    y1 --> s1 & s2
    y2 --> s3
    g1 --> s2 & s3
    g2 --> s1
    s1 --> r1
    s2 --> r2
    s3 --> r3
```
* Because we're doing an ***outer join***, keys which only have yellow taxi or green taxi records will be shown with empty fields for the missing data, whereas keys with both types of records will show both yellow and green taxi data.
    * If we did an ***inner join*** instead, the records such as `(K1, Y1, Ø)` and `(K4, Ø, G3)` would be excluded from the final result.

### Joining a large table and a small table

>Note: this section assumes that you have run the code in [the test Jupyter Notebook](../5_batch_processing/03_test.ipynb) from the [Installing spark section](#installing-spark) and therefore have created a `zones` dataframe.

Let's now use the `zones` lookup table to match each zone ID to its corresponding name.

```python
df_zones = spark.read.parquet('zones/')

df_result = df_join.join(df_zones, df_join.zone == df_zones.LocationID)

df_result.drop('LocationID', 'zone').write.parquet('tmp/revenue-zones')
```
* The default join type in Spark SQL is the inner join.
* Because we renamed the `LocationID` in the joint table to `zone`, we can't simply specify the columns to join and we need to provide a condition as criteria.
* We use the `drop()` method to get rid of the extra columns we don't need anymore, because we only want to keep the zone names and both `LocationID` and `zone` are duplicate columns with numeral ID's only.
* We also use `write()` instead of `show()` because `show()` might not process all of the data.

The `zones` table is actually very small and joining both tables with merge sort is unnecessary. What Spark does instead is ***broadcasting***: Spark sends a copy of the complete table to all of the executors and each executor then joins each partition of the big table in memory by performing a lookup on the local broadcasted table.

```mermaid
graph LR
    subgraph B [big table]
        b1[partition 1]
        b2[partition 2]
        b3[partition 3]
    end
    subgraph E [executors]
        subgraph E1 [executor 1]
            e1{{executor}} -.->|lookup| z1["zones (local)"]
            z1 -.->|return| e1
        end
        subgraph E2 [executor 2]
            e2{{executor}} -.->|lookup| z2["zones (local)"]
            z2 -.->|return| e2
        end
        subgraph E3 [executor 3]
            e3{{executor}} -.->|lookup| z3["zones (local)"]
            z3 -.->|return| e3
        end
    end
    subgraph R [result]
        r1[zone, ...]
        r2[zone, ...]
        r3[zone, ...]
    end
    z[zones]-.->|broadcast| z1 & z2 & z3
    b1-->e1-->r1
    b2-->e2-->r2
    b3-->e3-->r3
```

Shuffling isn't needed because each executor already has all of the necessary info to perform the join on each partition, thus speeding up the join operation by orders of magnitude.