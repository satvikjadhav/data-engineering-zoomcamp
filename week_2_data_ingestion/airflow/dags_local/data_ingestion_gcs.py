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

# Helps us interact with google cloud
from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

# Paths
# Importing enviornment values which we set up in our Docker Container while setting up docker
# These enviornment variables could be changed/modified/deleted in our docker-compose.yaml file
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data_all')


PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')


local_workflow = DAG(
    "data_ingestion_gcs",
    description="Ingesting data into a google cloud storage and bigQuery",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2021, 1, 1), 
    max_active_runs=1
)

url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv'


# URL Templating
URL_PREFIX = 'https://s3.amazonaws.com/nyc-tlc/trip+data'
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{execution_date.strftime(\'%Y-%m\')}}'
OUTPUT_FILE_TEMPLATE = path_to_local_home + '/output_{{execution_date.strftime(\'%Y-%m\')}}.csv'
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'
PARQUET_FILE = f'{OUTPUT_FILE_TEMPLATE}'.replace('.csv', '.parquet')


# Functions
def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


with local_workflow:


    wget_task = BashOperator(
        task_id = 'download_dataset',
        bash_command = f'curl -sSLf {url} > {OUTPUT_FILE_TEMPLATE}'
        # bash_command = 'echo "{{execution_date.strftime(\'%Y-%m\')}}"'
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{OUTPUT_FILE_TEMPLATE}",
        },
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{TABLE_NAME_TEMPLATE}.parquet",
            "local_file": f"{path_to_local_home}/{PARQUET_FILE}",
        },
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": f"{TABLE_NAME_TEMPLATE}",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{PARQUET_FILE}"],
            },
        },
    )

    clean_task = BashOperator(
        task_id = 'clean_local_files',
        bash_command = f'rm {PARQUET_FILE} {OUTPUT_FILE_TEMPLATE}'
    )

    wget_task >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task >> clean_task