## Ingesting Data to GCP with Airflow

### What is a DAG
- A DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run.
Typical Workflow Components

- Write our own pipeline to put data into a data lake in our own format

### Four main components to a Workflow:
1. DAG
	- Specifies dependencies between tasks
	- Specifies in which order the tasks are to be executed
	- All DAGs have a beginning task and a final (end) task
	- Parametrized by always including an interval
	- We can also include default arguments

2. Task
	- Defined unit of work
	- Known as "Operators" in Airflow
	- Describe what to do
	- Tasks could be either upstream tasks or downstream tasks
	- Airflow sends out tasks to run on workers when space becomes available
		- No guarantee if a all the tasks will run on the same worker or on the same machine

3. DAG Run
	- An individual execution or run of a DAG

4. Task Instance
	- Individual run or execution of a task
	- Have an indicative state

### Sensors
- Entire subclass of operators which are all about waiting for an external event to happen

### Best practice is to have atomic operators
- Operators that can stand on their own, and do not need to share resources among others

### Every single operator must be defined to a DAG, either within the with operator or by passing the dag_id into each of the operators.

### To pass data between tasks, we have two options:
1. XCom Variable
	- Push and pull small bits of metadata

2. Upload and Download large files from a storage service
	- This is what we will be using

### Now we will be attaching functions to operators in our DAGs

- format_to_parquet
- upload_to_gcs 

