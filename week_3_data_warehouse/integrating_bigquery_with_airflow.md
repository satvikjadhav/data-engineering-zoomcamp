## Workshop: Integrating BigQuery with Airflow

### Problem Statement:
- Automating the steps we learned in week 3 with Airflow pipelines

### Our pipeline will do the following:

1. Move the respective taxi data (yellow/green) to respective color folder
2. Crate an external table in BigQuery from the files in GCS
3. Create partitioned tables in BigQuery

We can execute any SQL queries by using BigQueryInsertJobOperator