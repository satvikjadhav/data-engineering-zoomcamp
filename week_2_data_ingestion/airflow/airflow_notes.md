## Setting up Airflow Locally

### Airflow has the following components:
1. Scheduler
	- Responsible for scheduling jobs. Handles both triggering & scheduled workflows, submits Tasks to the executor to run, monitors all tasks and DAGs, and then triggers the task instances once their dependencies are complete.
2. Executor
3. Metadata Database
	- Backend to the Airflow environment. Used by the scheduler, executor and webserver to store state.
4. Workers
	- This component executes the tasks given by the scheduler.
5. DAG Directory
6. Webserver
	- GUI to inspect, trigger and debug the behaviour of DAGs and tasks. Available at http://localhost:8080.

### Other components (seen in docker-compose services):
- redis: Message broker that forwards messages from scheduler to worker.
- flower: The flower app for monitoring the environment. It is available at http://localhost:5555.
- airflow-init: initialization service (customized as per this design)

### Airflow Setup via Docker

1. Create a new sub-directory called airflow in your project dir (such as the one we're currently in)

2. Import the official image & setup from the latest Airflow version:
	- curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
3. It could be overwhelming to see a lot of services in here. But this is only a quick-start template, and as you proceed you'll figure out which unused services can be removed. Eg. Here's a no-frills version of that template.

4. Set the Airflow user:

	- On Linux, the quick-start needs to know your host user-id and needs to have group id set to 0. Otherwise the files created in dags, logs and plugins will be created with root user. You have to make sure to configure them for the docker-compose:

		- mkdir -p ./dags ./logs ./plugins
		- echo -e "AIRFLOW_UID=$(id -u)" > .env

	- On Windows you will probably also need it. If you use MINGW/GitBash, execute the same command.

	- To get rid of the warning ("AIRFLOW_UID is not set"), you can create .env file with this content:

	- AIRFLOW_UID=50000

5. Docker Build

	- When you want to run Airflow locally, you might want to use an extended image, containing some additional dependencies - for example you might add new python packages, or upgrade airflow providers to a later version.

	- Create a Dockerfile pointing to Airflow version you've just downloaded, such as apache/airflow:2.2.3, as the base image
	- And customize this Dockerfile by:
		1. Adding your custom packages to be installed. The one we'll need the most is gcloud to connect with the GCS bucket/Data Lake.
		2. Also, integrating requirements.txt to install libraries via pip install

	- enter docker-compose build in the airflow folder
	- we only need to run the build command whenever there is a change in the dockerfile

	- now we will run the airflow initialization service:
		- docker-compose up airflow-init

	- now that the initialization has been done, we now initiate the other services such as the back-end, scheduler, worker and the rest. 
		- docker-compose up

	- To immediately stop/kill all running Docker containers by using the following command:
		- docker kill $(docker container ls -q)
		- We can also use "stop" instead of "kill" to gracefully stop the running containers

6. Docker Compose:

	- Back in your docker-compose.yaml:
		1. In x-airflow-common
			- Remove the image tag, to replace it with your build from your Dockerfile, as shown
			- Mount your google_credentials in volumes section as read-only
			- Set environment variables GOOGLE_APPLICATION_CREDENTIALS and AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT
		2. Change AIRFLOW__CORE__LOAD_EXAMPLES to false (optional)
