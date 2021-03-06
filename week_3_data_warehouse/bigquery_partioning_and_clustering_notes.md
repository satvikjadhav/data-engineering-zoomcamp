## Partitioning and Clustering

### BigQeury Partitioning

We can partition on the following column when creating a partition table
- Time-unit column
	- Daily
	- Hourly
		- If we have tons of data coming in
		- And we want to process our data hourly
	- Monthly
	- Yearly
- Ingestion time
	- Daily
	- Hourly
	- Monthly
	- Yearly
- Integer range partitioning

Number of partitions limit is 4000 in bigQuery

### BigQueyr Clustering

1. The columns we specify are used to colocate the related data
	- The order of the column is very important here because this is the order that specifies the sort order of the data
		- If we are clustering on columns A, B, and C
		- The sort order would be starting from column A, then B, then C

2. Clustering generally improves:
	- Filter Queries
	- Aggregate queries
	- Specially on if we are running filter and aggregate queries on the columns we have specified our clustering on

3. If your table/data size is less than 1 G.B., then there won't be significant improvement with partitioning and clustering
	- They might add add significant cost instead
	- Incur metadata reads and metadata maintenance

4. We can specify up to four clustering columns

5. Clustering columns must be top-level, and non-repeated columns
	- Types of columns we can use for clustering
		- DATE
		- BOOL
		- GEOGRAPHY
		- INT64
		- NUMERIC
		- BIGNUERIC
		- STRING
		- TIMESTAMP
		- DATETIME

### Partitioning vs Clustering

1. Clustering
	- Cost benefit unknown
	- We need more granularity than partitioning alone allows
	- Our queries commonly use filters or aggregation against multiple particular columns
	- The cardinality of the number of values in a column or group of columns is large

2. Partitioning
	- Cost known upfront
	- You need partition-level management
	- Filter or aggregate on single column

#### When will we chose clustering over partitioning

1. We will be using clustering over partitioning when the partitioning results in a small amount of data per partition (less than 1 G.B.)

2. Partition results in a large number of partitions (> 4000 for example)

3. Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (for example, every few minutes)
	- Writing data to our bigQuery table that modifies the partitions then it might not be a good idea to use partitioning

#### Automatic Re-clustering by BigQuery
	This does not cost the end user anything as its done in the background

As data is added to a clustered table

- this newly inserted data can be written to blocks that contain key ranges
- These key ranges overlap with the key ranges in previously written blocks
- These overlapping keys weaken the sort property of the table
- As a result our query time can increase

To maintain the performance characteristics of a clustered table

- BigQuery performs automatic re-clustering in the background
- This is done to restore the sort property of the table
- For partitioned tables, clustering is maintained for data within the scope of each partition