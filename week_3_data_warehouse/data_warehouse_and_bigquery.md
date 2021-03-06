## [Data Warehouse and BigQuery Notes](https://www.youtube.com/watch?v=jrHljAoD6nM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=26)

### Data Warehouse 
	We will be using BigQuery mainly

### Online Analytical Processing (OLAP) vs Online Transaction Processing (OLTP)
	OLAP databases are mainly used by analysts and for analytical purposes

#### OLTP
- **Purpose**
	- Control and run essential business operations in real time

- **Data updates**
	- Short, fast updates initiated by user

- **Database design**
	- Normalized databases for efficiency

- **Space requirements**
	- Generally small if historical data is archived

- **Backup and recovery**
	- Regular backups required to ensure business continuity and meet legal and governance requirements

- **Productivity**
	- Increases productivity of end users

- **Data View**
	- Lists day-to-day business transactions

- **User Examples**
	- Customer-facing personnel, clerks, online shoppers

#### OLAP
- **Purpose**
	- Plan, solve problems, support decisions, discover hidden insights

- **Data updates**
	- Data periodically refreshed with scheduled, long-running batch jobs

- **Database design**
	- Denormalized databases for analysis

- **Space requirements**
	- Generally large due to aggregating large datasets

- **Backup and recovery**
	- Lost data can be reloaded from OLTP database as needed in lieu of regular backups

- **Productivity**
	- Increases productivity of business managers, data analysts, and executives

- **Data View**
	- Multi-dimensional view of enterprise data

- **User Examples**
	- Knowledge workers such as data analysts, business analysts, and executives


### What is a Data Warehouse?

- It is an OLAP solution
- Used for reporting and data analysis
- Generally consists of Meta Data, Summary Data, and Raw Data
- Data Warehouses can have many sources such as different operational systems, or other databases, or flat file systems
- Used by data analysts or data scientists

### BigQuery
	This is a data warehouse solution by Google

- It is a serverless data warehouse
	- There are no servers to manage or database software to install
	- simple plug and play concept
	- When a company starts its journey in the data storage solution, a huge chunk of time and money is spent on creating, setting up, and maintaining of the servers
	

- Provides software as well as infrastructure
	- Has scalability and high-availability 
	- We can start with few gigabytes of data and scale to petabytes of data without any issues

- Built-in features like:
	- Machine Learning
	- Geospatial Analysis
	- Business Intelligence

- BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage
	- So if needed we can upgrade the compute engine without having to touch our storage solution

- BigQuery generally caches the results


- **Cost**
	- On Demand Pricing
		- Based on the amount of data scanned or processed
		- 1 TB of data processed is $5

	- Flat Rate Pricing
		- Based on number of pre requested slots
		- 100 slots -> $2,000/month = 400 TB data processed on demand pricing
		- We also have to keep in mind about queries competing with each other

- BigQuery infers the data we are trying to import in; column names, their respective types, and if they are nullable or not

- When we use external data to create tables, bigQuery is not able to determine its row size or the table size
	- This is because the data itself is not inside bigQuery

### Partitions and Clustering

- **Partitioning**
	- Generally when we create a dataset, there are columns that are used the most
	- For example if we want using the date column alot and we partition the table on date column, it can improve the query performance by a lot
	- This is really good for bigQuery as now bigQuery will only process the data in that specific partition as opposed to processing all of the data

- **Clustering**
	- We can also cluster the tables according to a column (For example the "Tags" column in stackoverflow questions table)
	- example in the queries.sql file
	- The choice of using which column as for clustering is dependent on how we want to query our data

### Best Practices

We are generally concerned with cost reduction or improving query performance

1. **Cost Reduction**
	- Avoid the use of SELECT * queries
		- BigQuery stores data in a columnar storage format, so its better to query specific columns
	- Price your queries before running them
	- Use clustered or partitioned tables
	- Use streaming inserts with caution
	- Materialize query results into different stages

2. **Query Performance**
	- Filter on partitioned columns
	- Denormalized data
	- Use nested or repeated columns
		- This will help in denormalizing our data
	- Use external data sources appropriately
		- Might incur more cost while reading from google cloud storage for example
	- Don't use it, in case you want a high query performance
	- Reduce data before using a JOIN clause
	- Do not treat WITH clauses as prepared statements
	- Avoid over sharding tables
	- Avoid JavaScrip user-defined functions
	- Use approximate aggregation functions (HyperLogLog++)
	- Order Last, for query operations to maximize performance
	- Optimize your join patterns
	- As a best practice
		- Place the table with the largest number of rows first
		- followed by the table with the fewest rows
		- Then place the remaining tables by decreasing size
		- Reason for this is:
			- If we place the large table first, it will get distributed evenly
			- And the second table will be broadcasted to all the nodes

### Internals

- High level architecture picture of bigQuery is in the [pdf file](https://github.com/satvikjadhav/data-engineering-zoomcamp/blob/main/week_3_data_warehouse/data_warehouse_ppt.pdf)

> Knowing the internals of a data warehouse solution such as bigQuery will possibly help in building a data product

1. BigQuery stores our data in a separate storage known as **"Colossus"**
	- Colossus is a cheap storage base
	- Stores data in a columnar format
	- This has big advantage
		- Because bigQuery is now separating the storage from compute, and as a result has significantly less cost
		- If our data size increases tomorrow we only have to pay for the storage in Colossus

**Most of the cost is incurred while reading the data or running the queries, which is compute based**

2. But because the storage and the compute are on different hardware, how do they communicate with each other?
	- If the network, for example, is very bad it will result in high query time
		- This can be a very big disadvantage
	- For this the "Jupiter" network is used
	- The Jupiter network is inside bigQuery data centers
	- This network provides approximately 1 T.B. / Sec network speed. 

3. The third part of the bigQuery architecture is the **"Dremel"**
	- This is known as the query execution engine
	- It generally divides our query into a tree structure
		- Root Nodes
		- Intermediate nodes/Mixers
		- Leaf nodes (Local storage)
	- And separates our query in such a way that each node can execute an individual subset of the query

	- How does **Dremel** actually work?
		- First the root server receives our query. It then understands this query and divides into smaller sub modules
			- Here the query is modified and may change
		- It further divides the query further to R1 to R1n
		- The mixers now get the modified queries which is then further divided into other modified queries
		- These modified queries are then given to the Leaf Nodes
		- The Leaf Nodes communicate with the Colossus database
			- They fetch the data from Colossus
			- Executes the appropriate actions on that data
			- And returns the data/result to Mixers, which then return the respective data/result to Root server 
			- And finally the data is aggregated and returned as a result
		- The distribution of the workers is the reason why bigQuery is so fast

		- If all this was not done, and it was all done on a particular node, it will increase the query time with respect to the data size


### Column-oriented vs Record-oriented storage

**Record-orientated (row)**
- CSVs
- easy to process and understand

**Column-oriented**
- The columns in a row are now re-organized
- There will be multiple columns associated with rows
- Helps us provide better aggregations on columns 


### Machine Learning in BigQuery

Target audience Data Analysts, Managers
No need for Python or Java knowledge
No need to export data into a different system
- We can build the data model in the data warehouse itself (BigQuery)

#### ML in BigQuery Pricing

- Free Tier
	- 10 GB per month of data storage
	- 1 TB per month of queries processed
	- ML Create model step: first 10 GB per month is free

#### Steps involved in machine learning

- Data Collection
- Data Processing / Feature Engineering
- Data splitting: Training and Test data sets
- ML Model Training
- ML Model Validation
- Deployment

Explain and Predict function in BigQuery ML is helpful when we want to know the top n features used in our dateset and in prediction. 