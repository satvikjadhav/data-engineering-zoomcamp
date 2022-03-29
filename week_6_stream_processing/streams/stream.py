import faust
from taxi_rides import TaxiRide

# The app defines the stream ID
app = faust.App('de.stream.v2', broker='kafka://localhost:9092')
topic = app.topic('de.yellow_taxi_ride.json', value_type=TaxiRide) # The value_type is essentially a schema for the messages


@app.agent(topic)
async def start_reading(records):
    async for record in records:
        print(record)


if __name__ == '__main__':
    # main basically goes into the agent
    # which reads the data from topic we feed it. In our case its line 6
    app.main()