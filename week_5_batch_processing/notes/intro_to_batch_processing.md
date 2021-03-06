# Introduction to Batch Processing

## Different ways to process data
		Batch vs Streaming

- **Batch**
	- One single `job` that takes a set amount of data, which is then transformed or some new data is produced
	- This could be done in intervals of months, weeks days, hours, or every 5 minutes
- **Streaming**
	- Processing of data in real time
	- `Events`
	- When booking a taxi, for example, the confirmation and notifications are processed in real time

### Technologies
- Python Scripts
	- Can be run in: Kubernetes, Spark
- SQL
- Spark
- Flink

## Advantages and Disadvantages of Batch Jobs

**Advantages**
- Easy to manage
- Convenient to retry 
- Easier to scale

**Disadvantages**
- Delay


## Preparing Yellow And Green Taxi Data


First, let's download the Jan, 2021 data for Yellow and Green Taxi trips
- https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
- https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2021-01.csv

Now, lets create a simple bash script to download the data
```bash
# $1, and $2 mean the first and second values we give this script from the command line
TAXI_TYPE=$1 #"yellow"
YEAR=$2 #2020

set -e

# https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
# https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2021-01.csv

URL_PREFIX="https://s3.amazonaws.com/nyc-tlc/trip+data"


for MONTH in {1..12}; do
	FMONTH=`printf "%02d" ${MONTH}`

	URL="${URL_PREFIX}/${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.csv"

	LOCAL_PREFIX="/home/satvikjadhav/notebooks/data/raw/${TAXI_TYPE}/${YEAR}"
	LOCAL_FILE="${TAXI_TYPE}_tripdata_${YEAR}_${FMONTH}.csv"
	LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

	mkdir -p ${LOCAL_PREFIX}
	wget ${URL} -O ${LOCAL_PATH}

	#gzip ${LOCAL_PATH}
done

```

In `wget` we use `-O` to specify where we want to save the downloaded fine

To see our tree structure, we can run the following commands:
```bash
sudo apt-get install tree

tree folder_name
```

