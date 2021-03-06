## Workflow Orchestration

### What is a data pipeline?
- A script or a batch of script that takes in one or more data sources, processes this data, and produces transformed or modified data.
	- Take data
	- Modify this data
	- Save this data somewhere

### Basic Ideas
- Each job should do only one task; there shouldn't be more than one task in one job

- We would want to create multiple files that each do the respective tasks. 

### Sample complex data pipeline:
- WGET to download csv file
- convert csv to parquet file
- upload this to google cloud storage
- take the parquet files and upload to the BigQuery

### DAG: Directed Acyclic Graph
- Jobs are directed
- There are no cycles or loops

### Workflow Orchestration Tools
- Apache Airflow
- Luigi
- Prefect
- Dagster
