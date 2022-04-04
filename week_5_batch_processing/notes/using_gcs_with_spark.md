# Connect Spark to Google Cloud Storage (DataLake)

To upload any file or folder from our Google VM to our Google Cloud Storage, we can use the following command in terminal:
```bash
gsutil cp -m -r pq/ gs://dtc_data_lake_data-engineering-339113/pq
```

Here the following flags are: 
**r**: for recursive flag. We want to upload all the files in a folder
**m**: multi threaded. We want to upload the files in parallel so the process will be faster 

## Connect to Google Cloud Storage

1. IMPORTANT: Download the Cloud Storage connector for Hadoop here: https://cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage#clusters
- As the name implies, this .jar file is what essentially connects PySpark with your GCS
- In order to download it into our own Google VM we can use the following command:
```bash
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar
```

2. Move the .jar file to your Spark file directory.
- MacOS example: create a /jars directory under "/opt/homebrew/Cellar/apache-spark/3.2.1/ (where my spark dir is located)

3.  In our Python script, there are a few extra classes we will have to import:
```python
import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
```

4. Set up your configurations before building your SparkSession. Here’s an example code snippet:
```python
conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "/opt/homebrew/Cellar/apache-spark/3.2.1/jars/gcs-connector-hadoop3-latest.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "path/to/google_credentials.json")

sc = SparkContext(conf=conf)

sc._jsc.hadoopConfiguration().set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
sc._jsc.hadoopConfiguration().set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
sc._jsc.hadoopConfiguration().set("fs.gs.auth.service.account.json.keyfile", "path/to/google_credentials.json")
sc._jsc.hadoopConfiguration().set("fs.gs.auth.service.account.enable", "true")
```

5. Now, build `SparkSession` with the new parameters we’d just instantiated in the previous step
```python
spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()
```

6. Finally, we are able to read your files straight from GCS!
```python
df_green = spark.read.parquet("gs://{BUCKET}/green/202*/")

```