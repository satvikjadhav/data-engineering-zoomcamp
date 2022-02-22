## [Building dbt](https://www.youtube.com/watch?v=UVI30Vxzd6c&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=39)

### Anatomy of a dbt Model
	Models are shuffle select essentially, so the transformation or the business logic we are going to translate it to is a select statement

1. A dbt model is a SQL file
	- Has double curly brackets (also known as jinja templating)
		- we can use functions or macros in these
	- this is where we write our select statements
2. Several materialization strategies (most common ones)
	- Table
	- View
	- Incremental
		- Useful for data that doesn't change everyday
	- Ephemeral
3. dbt then runs this compiled code in the data warehouse

### The FROM Clause of a dbt Model

#### Sources (in a select statement)
- The data loaded to our data warehouse that we use as sources for our model
- These sources are are defined in the yml files in the models folder
```yaml
sources:
	- name: staging
		database: production
		schema: trip_data_all
		tables:
			- name: green_tripdata
```
- This would look like: 
```sql
select * from {{source('staging', 'green_tripdata')}}
```
- this will be translated to:
```sql
select * from production.trip_data_all.green_tripdata
```
- This will also take care of all the dependencies at the end
- In one schema and database, we can define as many tables as we want and sources as well
- Source freshness can be defined and tested via `freshness`

Seeds
	Nothing more than a copy command
- CSV files stored in our repository under the seed folder
- Benefits of version controlling
	- These CSV files will be in our repository
- Recommended for data that does not change frequently
- Runs with `dbt seed -s file_name`
- Used with the 'ref' macro

Ref
- Macro to reference the underlying tables and views that were building the data warehouse
- Run the same code in any environment, it will resolve the correct schema for you
- Dependencies are build automatically
dbt model:
```sql
with green_data as (
	select *, 
		'Green' as service_type
	from {{ ref('stg_green_tripdata') }}
	)
```
compiled code:
```sql
with green_data as (
	select *, 
		'Green' as service_type
	from "database_name"."schema_name"."stg_green_tripdata"
	)
```

### Defining a source and developing the first model (stg_green_tripdata)

Let's first create two new folders under the `models` folder in our dbt project (taxi_rides_ny)
#### 1. Staging
- in this we are going to be creating our raw models
- taking the raw data in views/tables, applying some typecasting, renaming, adding a derived table
- create our model file: `stg_green_tripdata.sql`
	- When creating the query, we should use the `source` macro as it will build the necessary dependencies and
	- And also resolve the appropriate schema for us
- create `schema.yml` in this folder  
	- **remember to but a line before `version: 2` so the `schema.yml` file will work**
	- In this we define the source, database(project name), and schema (dataset)
	- And we can have as many tables under this source as we want
	- in the `tables` we define the name of tables that we want to use as `sources` in our `model`
- In sources we can also define `freshness`
	- Use field that is used to load that data
- Source marco: `source('source_name'.'table_name')`
- model query written: 
```sql
select * from {{ source('staging','green_taxi') }}
limit 100
```
- query compiled by dbt:
```sql
select * from `data-engineering-339113`.`trips_data_all`.`green_taxi`
limit 100
```


#### 2. Core
- in the we are going to create models that will be shared with stakeholders 
- exposed to the bi tool 
- models that we want in production

### Definition and Usage of Macros
	We can define our own macros

- Use control structures (if statements and for loops for example) in SQL
- Use environment variables in your dbt project for production deployment
- Operate on the results of one query to generate another query
- Abstract snippets of SQL into reusable macros
	- these are analogous to functions in most programming languages

In a macro, it would return the code to do something, for example concatenating string a and b
- This is very helpful when we want to maintain the same type of information in all our models

To define a macro, we create a separate file under the `macros` folder in our dbt project
- We will be using a combination of Jinja and SQL

The follow code snippets demonstrate how this works in dbt:

Definition of the macro
```sql
{#
    This macro returns the description of the payment_type 
#}

{% macro get_payment_type_description(payment_type) -%}

    case {{ payment_type }}
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
    end

{%- endmacro %}
```

Usage of the macro
```sql
select
	{{ get_payment_type_description('payment_type') }} as payment_type_description,
	congestion_surcharge::double precision
from {{ source('staging', 'green_taxi') }}
where vendorid is not null
```

Compiled code of the macro
```sql
create or alter view `data-engineering-339113`.`dbt_satvik`.`stg_green_tripdata` as 
select
	case payment_type
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
    end as payment_type_description,
    congestion_surchage::double precision
from data-engineering-339113.trips_data_all.green_taxi
where vendorid is not null
```

In the `targets` folder we will find all the compiled code as well. 

Its also very useful to know that we could also use `macros` from other projects in our projects 
- The way to do this is by using dbt packages

Importing and Using dbt Packages

Packages
- Like libraries in other programming languages
- Standalone dbt projects, with models and macros that tackle a specific problem area
- By adding a package to our project, the package's models and macros will become part of our project as well 
- Imported in the `packages.yml` file in the main directory of our project, and imported by running `dbt deps`

To call a macro that we import from a package we do the following in the Jinja template
- `dbt_utils.surrogate_key()`

### What are Variables and setting them via CLI

**Variables**
- variables are useful for defining values that should be used across the project
- With a macro, dbt allows us to provide data to models for compilation
- To use a variable we use the `{{ var('...') }}` function
- Variables can be defined in two ways:
	- In the `dbt_project.yml` file
	- On the command line

We will be able to get data from variables via macros and use this during the compilation time

### Creating and using dbt Seeds
	dbt seeds are csv files that we can have in our repo and run and use as tables

dbt seeds are meant to be used with files that are smaller files and have data that will not change

1. create the `seeds` folder in our dbt project directory if its not there already
2. Add the csv file in this folder
3. run `dbt seed`
- This will create a table for the csv files in our database
- `dbt run` will not run the seeds
- If we want to also run the seed then we can use `dbt build --select +model_name`
	- By using the `+` symbol here, it will also build all the dependencies (models + seeds) for that model

And if we don't like the column types that it interprets, we can define it in the `dbt_project.yml` file as follows:
```yaml
seeds: 
  taxi_rides_ny:
    taxi_zone_lookup:
      +column_types:
        locationid: numeric
```

If we change a value on the csv file and when `dbt seed` is ran, it would end up creating a new line with that change
- to avoid this we run: `dbt seed --full-refresh`
	- this will drop the table, and create a new one

Ideally we want our `core` or `production` models to be `table` based
- this is because they will be exposed to our BI tools and its much more efficient

By using `{{ ref('taxi_zone_lookup') }}` it would create a model that is now dependent on our `seed` `taxi_zone_lookup`