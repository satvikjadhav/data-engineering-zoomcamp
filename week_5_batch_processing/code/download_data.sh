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