## [What is dbt?](https://www.youtube.com/watch?v=4eCouvVOJUw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=35)

### What is dbt?
- data build tool (dbt)
- dbt is a data transformation tool
- Allows anyone that knows SQL to deploy analytics code
- Follows software engineering best practices like modularity, portability, CI/CD, and documentation.

### Stages in dbt
1. Development
	- Develop our models
2. Test and Document models
3. Deployment
	- Version Control
	- CI/CD

### How does dbt work?

1. We are adding a "Modeling Layer" known as a model on top of our data warehouse. 
	- This is where we will be transforming the data
2. The derived model that we get will be persisted back to the Data Warehouse
3. Each model file is:
	- a .sql file
	- Select statement, no DDL or DML
	- A file that dbt will compile and run in our Data Warehouse
4. dbt will compile the model file by creating a DDL or DML file 
5. Finally, push that compute to our Data Warehouse
6. We will now be able to see a table or a view in our Data Warehouse

### How to use dbt?

#### dbt Core
- Essence of dbt
- open-source project that allows the data transformation
	- Open source and free to use
- part of dbt that will build and run projects 
	- .sql and .yml files
- Includes SQL compilation logic, macros and several database adapters
- Includes a CLI interface to orun dbt commands locally

#### dbt Cloud
- Web Application
- SaaS application to develop and manage dbt projects
- Web-based IDE to develop, run and test dbt projects
- Jobs orchestration
- Logging and Alerting
- Integrated documentation
- Free for individuals
	- one developer seat

### How are we going to be using dbt?

#### BigQuery
- Development using cloud IDE
- No local installation of dbt core
- Optionally could use a local installation of dbt as well
	- need to install the latest version (1.0) with the BigQuery adapter (dbt-bigquery

#### PostgreSQL
- Development using a local IDE of our choice
- Local installation of dbt Core connecting to the PostgreSQL database 
- Running dbt models through the CLI 