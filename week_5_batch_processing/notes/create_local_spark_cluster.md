# Creating a Local Spark Cluster

When we use `local[*]` when creating a spark session, what it is doing under the hood is creating a local spark cluster and then we connect to it via `localhost:4040`

But if we shutdown the jupyter notebook then our spark cluster also turns off

Now we will start `spark` in standalone mode.

1. Got to spark installation directory
```bash
echo $SPARK_HOME
```
2. Go to the location of spark home
3. Then enter the following command
```bash
./sbin/start-master.sh
```

Now, if we want to connect to this spark master we would enter the following instead of `local[*]`: 
```python
spark = SparkSession \
		.builder.master('spark://data-spark.asia-south1-c.c.data-engineering-339113.internal:7077') \
		.appName('Spark Master') \
		.getOrCreate()
```

If we try to read a file we would get the following error
```
22/04/05 17:51:13 WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources
```
This is because we have zero workers. We only have the `master` available, and need something to take care of everything else. 

Now, to start a worker we can do the following
1. Got to spark installation directory
```bash
echo $SPARK_HOME
```
2. Go to the location of spark home
3. Then enter the following command
```bash
./sbin/start-worker.sh <master-spark-URL>
```
4. And after we are done we can stop the `master` and `slave` using the following commands
```bash
./sbin/stop-master.sh 
./sbin/stop-slave.sh 
```

Note: in older version of spark it is referred to as `slave` instead of `worker`

If we want to make our pyspark script configurable, the best way to do that is via CLI. 
For this we can use the `argparse` library

We can run the following command
```bash
python spark_local_sql.py --input_green=data/pq/green/* --input_yellow=data/pq/yellow/taxi_data/* --output=data/report/test
````

Now, imagine if we have multiple clusters. 
We cannot just specify the `spark master` URL inside the script every time. 

The best way is to specify the configuration outside of the python script. 
To do this we use `spark-submit`

***spark-submit*** is a script that comes with `spark` which is used to submit spark jobs to spark clusters

Example `spark-submit` command:
```bash
URL=spark://data-spark.asia-south1-c.c.data-engineering-339113.internal:7077

spark-submit --master="${URL}" /home/satvikjadhav/data-engineering-zoomcamp/week_5_batch_processing/code/spark_local_sql.py --input_green=/home/satvikjadhav/notebooks/data/pq/green/2021/* --input_yellow=/home/satvikjadhav/notebooks/data/pq/yellow/new_data/2021/* --output=/home/satvikjadhav/notebooks/data/report/test
```
