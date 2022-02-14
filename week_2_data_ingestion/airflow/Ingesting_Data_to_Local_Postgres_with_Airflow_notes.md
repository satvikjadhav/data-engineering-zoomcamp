## Ingesting data to Local PostgreSQL with Airflow

Converting the data ingestion script for loading data to Postgres to an Airflow DAG

Step by step take the workflow/data pipeline we created in week one (data ingestion pipeline), and put that inside Airflow as a DAG file
- Steps taken to convert the ingest_data.py script into a DAG file


**This will be split into two steps:**
1. Get the csv files
2. Ingest this csv files into our postgres database

We can do this both in our local/personal computer or in a VM on cloud

### Plan:

	1. Start with the docker-compose we had created in week_2/airflow folder
	2. Change the dag mappings
		- Here we would go in the "volumes:" section of the docker-compose file
		- and change ./dags:/opt/airflow/dags to ./dags_local:/opt/airflow/dags
			- the ":" after ./dags means we are mapping the file path /opt/airflow/dags to the ./dags file

	3. Make them run monthly
	4. Create a bash operator, and pass the params: ('execution_date.strftime(\'%Y-#m\')')
	5. Download the data using the code we had already written in previous Airflow activities in week_2
	6. Put the ingest script to Airflow
	7. Modify dependencies
		- Add the ingest script dependencies here
	8. Put the old docker-compose file in the same network

We now create our first empty dag file in our new folder (dags_local): data_ingestion_local.py

We should ideally give our task IDs longer names -- more descriptive of what the task is doing / trying too achieve

**When saving file in Airflow via wget, we cannot just save it in default location as that is temporary.**
- After the task is run, all the files in that temp folder will deleted. 
- To avoid this, we use something like: path_to_local_home/output.csv
- The path to local home can be taken via using the OS module

The L flag in "curl -sSL" is for making curl follow a redirect link

### Now we want to check where the file was downloaded in our Airflow

1. We first list out all our docker processes: docker ps
2. We are interested in the airflow-worker process here
3. We then enter the following command:
	- docker exec -it airflow-worker-container_id bash
		- by running this command we can now enter that container and check out the downloads and everything
	- wc -l output.csv 
		- command to get the total rows in a csv file

The problem with using output.csv as a name:

- Not a good name when we are running multiple DAGs in parallel, and they are downloading files

We want each task to write to its own output file and have unique names. 

Now, we want to get the execution date in YYY-MM format and put that in our URL.
- By doing this the URL will get updated with the YYY-MM of the task execution date and download the respective csv file for that month
- We are able to download month wise files, which is what we wanted

Now, let's put the ingestion script (ingest_data.py) from week 1 to Airflow

	1. We copy the ingest_data.py script from week one into dags_local
	2. Modify the script; we don't need the os command as well as the main namespace
	3. We first run the script using just the create_engine function to check we are able to connect to postgres
	4. To use pandas or any other library, we also need to have it installed on our airflow workers

	5. To add the modules to our workers, we can specify the required modules in the requirements.txt file or add in the Dockerfile
		- RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary
			- [--no-cache-dir] means that it will save not save to the cache
			- binary means that it will download the binary file and install using that

	6. Now that we have added the new modules, we need to build the docker containers again
		- docker-compose build

	7. Now we need to import our new ingest function from another script to our DAG file

	8. Now we need to pass parameters into our callable

	9. Previously we were passing the arguments via command line, bu this time we can the .env file
		- PG_HOST=pgdatabase
		- PG_USER=root
		- PG_PASSWORD=root
		- PG_PORT=5432
		- PG_DATABASE=ny_taxi

	10. Now we need to pass this information to workers
		- In docker-compose, in the environment tag
		- We add the above env variables here as well
		- PG_HOST: "${PG_HOST}"
	    - PG_USER: "${PG_USER}"
	    - PG_PASSWORD: "${PG_PASSWORD}"
	    - PG_PORT: "${PG_PORT}"
	    - PG_DATABASE: "${PG_DATABASE}"
	    - What this means is that the worker will have the above environmental variables 
	    - Which in turn will be read from the environmental variable of our host machine: PG_HOST: "${PG_HOST}"
	    - And these environmental variables will come from the .env file
	    - And because of the "&airflow-common-env" all airflow things will get it

    11. Now we add the following in our data_ingestion_local script:
    	- PG_HOST = os.getenv('PG_HOST')
		- PG_USER = os.getenv('PG_USER')
		- PG_PASSWORD = os.getenv('PG_PASSWORD')
		- PG_PORT = os.getenv('PG_PORT')
		- PG_DATABASE = os.getenv('PG_DATABASE')

	12. Now, how do we connect two different docker-compose yaml files? 
		- We have one in week_1 and another one in week_2
		- First get the network name by: docker network ls and copy the network name
		- Now add the following in the week_1 yaml file:
			networks:
			  airflow (we can put this to whatever name we want):
			    external:
			      name: my_network_name
		- and finally, add networks: airflow in the pgdatabase service
        - By doing this we can add the airflow network that is ran/created by our week_2 docker-compose yaml file

    13. For each month, we can have a separate table name
    	- TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'

    14. Reasons why we don't want to create one big table with all the csv files in it
    	- Idempotentcy
    		- All the tasks in airflow should be idempotent 
    		- The idea is it doesn't matter if we run the task once or 5 times or we ran it after it broke once
    		- After a successful run, we get our database in a state that is consistent

    15. This setup is okay for local testing, but in reality we would have: 
    	- Have a database running in the cloud
    	- For example, bigQuery or AWS Athena. And we insert our data there