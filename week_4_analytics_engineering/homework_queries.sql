-- Queries for creating fhv tripdata

CREATE OR REPLACE EXTERNAL TABLE `data-engineering-339113.trips_data_all.external_fhv_taxi`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_data-engineering-339113/raw/fhv_taxi_*.parquet']
);

-- Question 1
SELECT count(*) 
FROM `data-engineering-339113.dbt_satvik.fact_trips` 
WHERE pickup_datetime BETWEEN '2019-01-01' and '2020-12-31';
-- Answer: 61590796

-- Question 3
SELECT count(*) FROM `data-engineering-339113.dbt_satvik.stg_fhv_tripdata`
-- Answer: 42084899

-- Question 4
SELECT count(*) FROM `data-engineering-339113.dbt_satvik.fact_fhv_trips`
-- Answer: 22676253

-- Question 5
SELECT EXTRACT(MONTH FROM pickup_datetime), count(pickup_datetime) as rides
FROM `data-engineering-339113.dbt_satvik.fact_fhv_trips`
group by EXTRACT(MONTH FROM pickup_datetime)
order by rides
-- Answer: 3 (march)