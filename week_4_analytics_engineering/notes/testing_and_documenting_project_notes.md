## Testing and Documenting dbt Project
	Testing is not necessarily needed but is very much suggested to have in a mature project

### Tests
- Assumptions that we make about our data
- Tests in dbt are essentially a `select` sql query
- These assumptions get compiled to sql that returns the amount of failing records
- Tests are defined on a column in the .yml file
- dbt provides basic tests to check if the column values are:
	- Unique
	- Not null
	- Accepted values
	- A foreign key to another table
- We can create our own custom tests as queries
- Query how many records that do not follow the assumption we had made about our data

Definition of basic tests in the .yml files
```yaml
- name: payment_type_description
	description: Description of the payment_type code
	tests:
		- accepted_values:
			values: [1,2,3,4,5]
			severity: warn
``` 

Compiled code of the not_null test for example:
```sql
select *
from data-engineering-339113.dbt_satvik.stg_green_tripdata
where tripid is null
```
- `severity` lets the dbt know should it stop everything and warn us or continue running everything else

### Documentation

- dbt provides a way to generate documentation for dbt project
- It is rendered as a website that others can view/access
- The documentation for dbt project includes
	- Information about the project
		- Model code (both from the .sql file and compiled)
		- Model dependencies
		- Sources
		- Auto generated DAGs from the ref and source macros
		- Descriptions (from .yml file) and tests
	- Information about the data warehouse (information_schema)
		- Column names and data types
		- Table stats like size and rows
- dbt docs can also be hosted in dbt cloud

