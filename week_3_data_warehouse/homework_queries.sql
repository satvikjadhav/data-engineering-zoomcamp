-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `data-engineering-339113.nytaxi.external_fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_data-engineering-339113/raw/fhv_taxi_2019_*.parquet']
);

-- What is count for fhv vehicles data for year 2019?
select count(*) from `data-engineering-339113.nytaxi.external_fhv_tripdata`;
-- A: 42084899

-- How many distinct dispatching_base_num we have in fhv for 2019?
select count(distinct dispatching_base_num) from `data-engineering-339113.nytaxi.external_fhv_tripdata`;
-- A: 792

-- Create a partitioned table from external table 
CREATE OR REPLACE TABLE data-engineering-339113.nytaxi.external_fhv_tripdata_partitioned
PARTITION BY
  DATE(dropoff_datetime) AS
SELECT * FROM data-engineering-339113.nytaxi.external_fhv_tripdata;

-- Impact of Partition by dropoff_datetime
-- 379.8 MB
SELECT DISTINCT(dispatching_base_num)
FROM data-engineering-339113.nytaxi.external_fhv_tripdata
WHERE DATE(dropoff_datetime) BETWEEN '2019-01-01' AND '2019-02-01';

-- Partitioned table
-- 354.8 MB
SELECT DISTINCT(dispatching_base_num)
FROM data-engineering-339113.nytaxi.external_fhv_tripdata_partitioned
WHERE DATE(dropoff_datetime) BETWEEN '2019-01-01' AND '2019-02-01';

-- As noted in the video, the impact of partition is not as effective on a small size data

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE data-engineering-339113.nytaxi.fhv_tripdata_partitoned_clustered
PARTITION BY DATE(dropoff_datetime)
CLUSTER BY dispatching_base_num AS
SELECT * FROM data-engineering-339113.nytaxi.external_fhv_tripdata;

-- What is the count, estimated and actual data processed for query which counts trip between 2019/01/01 and 2019/03/31 for dispatching_base_num 'B00987', 'B02060', 'B02279'
SELECT COUNT(*)
FROM data-engineering-339113.nytaxi.fhv_tripdata_partitoned_clustered
WHERE DATE(dropoff_datetime) BETWEEN '2019-01-01' AND '2019-02-01'
AND dispatching_base_num IN ('B00987', 'B02060', 'B02279')
-- Count: 26643
-- Estimated: 400.1 MB
-- Actual: 141.9 MB

-- What will be the best partitioning or clustering strategy when filtering on dispatching_base_num and SR_Flag?
-- A: Cluster by dispatching_base_num and SR_Flag because we want to use clustering over partitioning when the partitioning results in a small amount of data per partition (less than 1 G.B.)