import os
import logging
from datetime import datetime

from airflow import DAG
from airflow.utils.dates import days_ago

# Importing our Operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Using this lib to for converting our csv files to parquet format
import pyarrow.csv as pv
import pyarrow.parquet as pq

# Importing our ingest function and script
from ingest_script import ingest_callable

#Paths
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

local_workflow = DAG(
    "data_ingestion_local",
    description="Ingesting data into a local postgres database",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2021, 1, 1), 
    max_active_runs=1
)

url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv'

URL_PREFIX = 'https://s3.amazonaws.com/nyc-tlc/trip+data'
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{execution_date.strftime(\'%Y-%m\')}}'
OUTPUT_FILE_TEMPLATE = path_to_local_home + '/output_{{execution_date.strftime(\'%Y-%m\')}}.csv'
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'

with local_workflow:


    wget_task = BashOperator(
        task_id = 'wget',
        bash_command = f'curl -sSLf {url} > {OUTPUT_FILE_TEMPLATE}'
        # bash_command = 'echo "{{execution_date.strftime(\'%Y-%m\')}}"'
    )

    ingest_task = PythonOperator(
        task_id = 'ingest',
        python_callable = ingest_callable,
        op_kwargs = dict(user=PG_USER,
                         password=PG_PASSWORD,
                         host=PG_HOST,
                         port=PG_PORT,
                         db=PG_DATABASE,
                         table_name=TABLE_NAME_TEMPLATE,
                         csv_name=OUTPUT_FILE_TEMPLATE)
    )

    clean_task = BashOperator(
        task_id = 'clean',
        bash_command = f'rm {OUTPUT_FILE_TEMPLATE}'
    )

    wget_task >> ingest_task >> clean_task