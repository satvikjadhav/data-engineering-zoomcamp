## Starting our dbt Project Locally: PostgreSQL and dbt Core Locally

### Creating a new dbt Project
1. **Using CLI**
	- After installing dbt locally and setting up profiles.yml (add link to this file), we run `dbt init`
		- `dbt init` creates a new repo called `dbt`
	- This should be run in the path we want to start the project
	- One of the important file is our dbt_project.yml file
	- We can specify different "profiles" to be used in dbt_project files

2. **Using dbt Cloud**
	- After setting up dbt Cloud credentials (repo and data warehouse), we can start the project from the web-based IDE

***dbt will write the DDL and DML queries for us***

In `dbt_project.yml` file we can define other settings that are global
- For example, in a given folder every model that is there is a `view` or a `table`
- We can also define global variables here

Sample `profile.yml`
```yaml
# defining our PostgreSQL database here

profile-name-here:
	target: dev
	outputs:
		dev:
			type: postgres
			host: localhost
			user: username
			password: password
			port: 5432
			dbname: production
			schema: schema_name
			threads: 4 # how many threads we want to use while running dbt locally
			keepalives_idle: 0 # default 0, indicating the system default

# defining our BigQuery data warehouse here

de-dbt-bq:
  outputs:
    dev:
      dataset: data-engineering-339113
      fixed_retries: 1
      keyfile: /.google/credentials/google_credentials.json
      location: asia-south1
      method: service-account
      priority: interactive
      project: data-engineering-339113
      threads: 2
      timeout_seconds: 300
      type: bigquery
  target: dev
```

In `dbt_project.yml` we can now change the `profile` name to the appropriate `profile` name from `profile.yml`