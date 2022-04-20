# Data Engineering Zoomcamp
## Repository to document my progress in the Data Engineering Zoomcamp course by DataTalks

### Week 1: Basics and Setup
- Docker
	- [Dockerfile](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_1_-_basics_and_setup/docker_sql/dockerfile)
	- Using [docker-compose](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_1_-_basics_and_setup/docker_sql/docker-compose.yaml) to start multiple containers
	- Setting up PostgreSQL via Docker
	- Dockerizing simple [python ingestion script](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_1_-_basics_and_setup/docker_sql/upload_data.py)
- [Terraform](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_1_-_basics_and_setup/terraform_gcp/Terraform_and_gcp_notes.md)
	- Setting up Terraform on local machine
	- Using Terraform to set up our Google Cloud services
	- Setting up Terraform files (main and variable)
- [Setting up Google Cloud Virtual Machine (VM)](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_1_-_basics_and_setup/terraform_gcp/setting_up_env_on_gcloud_cloud_vm_and_SSH_access_notes.md)
	- Setting up environment variables
	- Setting up SSH access and Config file
	- Setting up Docker
	- Setting up docker-compose
	- Setting up Terraform
	- Setting up pgcli
	- Setting up gcloud in our VM
	- Connecting VScode with VM
	- Port forwarding in VScode

### Week 2: Data Ingestion
- [Data Lake (GCS)](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/data_lake_notes.md)
- [Workflow Orchestration](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/workflow_orchestration_notes.md)
- [Setting up Airflow Locally via Docker](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/airflow/airflow_notes.md)
- [Ingesting data to GCP with Airflow](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/airflow/ingesting_data_to_gcp_with_airflow_notes.md)
- [Ingesting data to Local PostgreSQL with Airflow](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/airflow/Ingesting_Data_to_Local_Postgres_with_Airflow_notes.md)

### Week 3: Data Warehouse
- [Data Warehouse](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_3_data_warehouse/data_warehouse_and_bigquery.md)
	- Best Practices
	- Cost
	- Internals of BigQuery
	- ML in BigQuery
	- [BigQuery SQL queries](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_3_data_warehouse/queries.sql)
- [Partitioning and Clustering](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_3_data_warehouse/bigquery_partioning_and_clustering_notes.md)
- [Workshop: Integrating BigQuery with Airflow](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_3_data_warehouse/integrating_bigquery_with_airflow.md)
	- [GCS to BigQuery DAG](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_3_data_warehouse/airflow/dags/gcs_to_bq_dag.py)

### Week 4: Analytics Engineering
- [Analytics Engineering Basics](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/notes/analytics_engineering_basics.md)
- [What is dbt?](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/notes/what_is_dbt.md)
- [Building dbt](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/notes/building_dbt_notes.md)
- [Creating dbt Project Locally](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/notes/creating_dbt_project_locally_notes.md)
- [Testing and Documenting dbt Project](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/notes/testing_and_documenting_project_notes.md)
- [Deploying using dbt](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/notes/deployment_using_dbt_cloud.md)

### Week 5: Batch Processing
- [Batch Processing](week_5_batch_processing/notes/intro_to_batch_processing.md)
- [What is Spark](week_5_batch_processing/notes/intro_to_spark.md)
- [Spark Dataframes](week_5_batch_processing/notes/spark_dataframes.md)
- [Spark Internals](week_5_batch_processing/notes/spark_internals_notes.md)
	- Anatomy of a Spark Cluster
	- Group By in Spark
	- Joins in Spark
- Spark Setup
	- [Linux](week_5_batch_processing/notes/installing_spark_on_linux.md)
	- [PySpark on Linux](week_5_batch_processing/notes/setting_up_pyspark_on_linux.md)
- [Using GCS with Spark](week_5_batch_processing/notes/using_gcs_with_spark.md)

### Week 6: Stream Processing
- [Intro to Kafka](week_6_stream_processing/notes/intro_to_kafka.md)
- [Intro to Avro](week_6_stream_processing/notes/introduction_to_avro.md)
- [Kafka Config](week_6_stream_processing/notes/kafka_config.md)
- [Kafka Streams](week_6_stream_processing/notes/kafka_streams.md)
- [Kafka Connect and KSQL](week_6_stream_processing/notes/kafka_connect_and_ksql.md)