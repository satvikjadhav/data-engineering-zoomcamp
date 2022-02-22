## [Analytics Engineering Basics - Notes](https://www.youtube.com/watch?v=uF76d5EmdtU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=33)

### What is Analytics Engineering?

#### Data Domain Developments
1. **Massively Parallel Processing (MPP) databases**
	- Bigquery
	- Snowflake
	- Redshift
2. **Data-pipelines-as-a-service**
	- Fivetran
	- Stitch
3. **SQL-first**
	- Looker
4. **Version Control Systems** 
	- Looker
5. **Self Service Analytics**
	- Mode
	- Looker
6. **Data Governance**
	- Change the way the stakeholders are consuming the data


#### Roles in a Data Team
1. **Data Engineer**
	- Prepares and maintains the infrastructure that the data team needs
	- Great software engineers, but don't know how the data will be used by the business users
2. **Analytics Engineer**
	- Has a bit of both Data Engineering and Data Analytics
	- Introduces the good software engineering practices to the efforts of data analytics and data scientists
3. **Data Analyst**
	- Uses data to answer questions and solve problems
4. **Data Scientist**

However recently Data Analysts and Data Scientists are writing more and more code 

#### Tools Analytics Engineer Use
1. **Data Loading** - Airflow, Fivetran, Stitch
2. **Data Storing** - PostgreSQL, BigQuery, Snowflake, Redshift
3. **Data Modeling** - data build tool (dbt), Dataform
4. **Data Presentation** - BI tools like, Looker, Mode, or Tableau


### Data Modelling Concepts

#### ETL vs ELT
- **ETL: Extract, Transform, Load**
	- ETL takes longer to implement but results in cleaner data
	- ETL takes longer to implement but results in cleaner data
	- Higher storage and compute costs

- **ELT: Extract, Load, Transform**
	- The ELT approach enables faster implementation than the ETL process, though the data is messy once it is moved
	- The transformation occurs after the load function, preventing the migration slowdown that can occur during this process
	- Lower cost and lower maintenance
	- ELT decouples the transformation and load stages, ensuring that a coding error (or other error in the transformation stage) does not halt the migration effort
	- Additionally, ELT avoids server scaling issues by using the processing power and size of the data warehouse to enable transformation (or scalable computing) on a large scale.


#### Kimball's Dimensional Modeling

- **Objective**
	- Deliver data that is understandable to the business users 
	- Deliver fast query performance

- **Approach**
	- Prioritize user understandability
	- Prioritize query performance over non redundant data (3NF)

- **Other Approaches**
	- Bill Inmon
	- Data Vault


#### Elements of Dimensional Modeling

- **Star Schema**

1. **Facts Tables**
	- Measurements, metrics or just facts of our business
	- Corresponds to a business process
	- We can think of them more of as "verbs"; Sales or Orders

2. **Dimensions Tables**
	- Corresponds to a business entity/identity
	- Provides context to a business process
	- We can think of them more of as "nouns"; Customer or Product


#### Architecture of Dimensional Modeling
	- From Kimball's Dimensional Modeling
	- Kitchen Analogy 
	- Book compares how the data warehouse and the ELT process could be compared with a restaurant

1. **Stage Area**
	- Contains the raw data
	- Not exposed to everyone; only to people who know how to use this

2. **Processing Area - Kitchen in a restaurant**
	- From raw data to data models
	- Focuses in efficiency
	- Ensuring standards being followed
	- Limited only to people who know how to do the above steps

3. **Presentation Area - the Dining Hall**
	- Final presentation of the data
	- Exposure to business stakeholder
