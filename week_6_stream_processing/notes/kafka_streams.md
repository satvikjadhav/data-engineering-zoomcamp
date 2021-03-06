# Kafka Streams
	The idea is to process all the messages in a streaming fashion with milliseconds delay and not have a consumer mindset where we are consuming bulk of messages. 

## What is Kafka Streams?
	- Client library for building stream application
	- Data from Kafka to Kafka
	- Stream application
		- Fault tolerant
		- Scalable
	- Event processing with milliseconds latency
	- Provides a convenient DSL


[Kafka Streams](https://kafka.apache.org/documentation/streams/) is a _client library_ for building applications and services whose input and output are stored in Kafka clusters. In other words: _Streams applications_ consume data from a Kafka topic and produce it back into another Kafka topic.

Kafka Streams is fault-tolerant and scalable, and apps using the Streams library benefit from these features: new instances of the app can be added or killed and Kafka will balance the load accordingly. Streams can process events with latency of miliseconds, making it possible for applications to deal with messages as soon as they're available. Streams also provides a convenient [Domain Specific Language (Streams DSL)](https://docs.confluent.io/platform/current/streams/developer-guide/dsl-api.html) that simplifies the creation of Streams services.

Kafka Streams is both powerful and simple to use. Other solutions like Spark or Flink are considered more powerful but they're much harder to use, and simple Kafka consumers (like the ones we've created so far) are simple but not as powerful as apps using Streams. However, keep in mind that Streams apps can only work with Kafka; if you need to deal with other sources then you need other solutions.

 ## Streams vs State

When dealing with streaming data, it's important to make the disctinction between these 2 concepts:

* ***Streams*** (aka ***KStreams***) are _individual messages_ that are read sequentially.
* ***State*** (aka ***KTable***) can be thought of as a _stream changelog_: essentially a table which contains a _view_ of the stream at a specific point of time.
    * KTables are also stored as topics in Kafka.

![source: https://timothyrenner.github.io/engineering/2016/08/11/kafka-streams-not-looking-at-facebook.html](06_04.png)

## Streams Topologies and Features

A ***topology*** (short for _processor topology_) defines the _stream computational logic_ for our app. In other words, it defines how input data is transformed into output data.

Essentially, a topology is a graph of _stream processors_ (the graph nodes) which are connected by _streams_ (the graph edges). A topology is a useful abstraction to design and understand Streams applications.

A ***stream processor*** is a node which represents a processing step (i.e. it transforms data), such as map, filter, join or aggregation.

Stream processors (and thus topologies) are defined via the imperative Processor API or with the declarative, functional DSL. We will focus on DSL in this lesson.

Kafka Streams provides a series of features which stream processors can take advantage of, such as:
* Aggregates (count, groupby)
* Stateful processing (stored internally in a Kafka topic)
* Joins (KStream with Kstream, KStream with KTable, Ktable with KTable)
* [Windows](https://kafka.apache.org/20/documentation/streams/developer-guide/dsl-api.html#windowing) (time based, session based)
    * A window is a group of records that have the same key, meant for stateful operations such as aggregations or joins.

## Kafka Streams Demo - Intro

The native language to develop for Kafka Streams is Scala; we will use the [Faust library](https://faust.readthedocs.io/en/latest/) instead because it allows us to create Streams apps with Python.

1. `producer_tax_json.py` ([link](../streams/producer_taxi_json.py)) will be the main producer.
    * Instead of sending Avro messages, we will send simple JSON messages for simplicity.
    * We instantiate a `KafkaProducer` object, read from the CSV file used in the previous block, create a key with `numberId` matching the row of the CSV file and the value is a JSON object with the values in the row.
    * We post to the `datatalkclub.yellow_taxi_ride.json` topic.
        * You will need to create this topic in the Control Center.
    * One message is sent per second, as in the previous examples.
    
1. `stream.py` ([link](../streams/stream.py)) is the actual Faust application.
    * We first instantiate a `faust.App` object which declares the _app id_ (like the consumer group id) and the Kafka broker which we will talk to.
    * We also define a topic, which is `datatalkclub.yellow_taxi_ride.json`.
        * The `value_types` param defines the datatype of the message value; we've created a custom `TaxiRide` class for it which is available [in this `taxi_ride.py` file](../streams/taxi_rides.py)
    * We create a _stream processor_ called `start_reading()` using the `@app.agent()` decorator.
        * In Streams, and ***agent*** is a group of ***actors*** processing a stream, and an _actor_ is an individual instance.
        * We use `@app.agent(topic)` to point out that the stream processor will deal with our `topic` object.
        * `start_reading(records)` receives a stream named `records` and prints every message in the stream as it's received.
        * Finally, we call the `main()` method of our `faust.App` object as an entry point.
    * You will need to run this script as `python stream.py worker` .
1. `stream_count_vendor_trips.py` ([link](../streams/stream_count_vendor_trips.py)) is another Faust app that showcases creating a state from a stream:
    * Like the previous app, we instantiate an `app` object and a topic.
    * We also create a KTable with `app.Table()` in order to keep a state:
        * The `default=int` param ensures that whenever we access a missing key in the table, the value for that key will be initialized as such (since `int()` returns 0, the value will be initialized to 0).
    * We create a stream processor called `process()` which will read every message in `stream` and write to the KTable.
        * We use `group_by()` to _repartition the stream_ by `TaxiRide.vendorId`, so that every unique `vendorId` is delivered to the same agent instance.
        * We write to the KTable the number of messages belonging to each `vendorId`, increasing the count by one each time we read a message. By using `group_by` we make sure that the KTable that each agent handles contains the correct message count per each `vendorId`.
    * You will need to run this script as `python stream_count_vendor_trips.py worker` .
* `branch_price.py` ([link](../streams/branch_price.py)) is a Faust app that showcases ***branching***:
	* What we want to achieve is to consume some messages from our yellow taxi ride json, then publish it into a different topic based on some defined conditions
    * We start by instancing an app object and a _source_ topic which is, as before, `datatalkclub.yellow_taxi_ride.json`.
    * We also create 2 additional new topics: `datatalks.yellow_taxi_rides.high_amount` and `datatalks.yellow_taxi_rides.low_amount`
    * In our stream processor, we check the `total_amount` value of each message and ***branch***:
        * If the value is below the `40` threshold, the message is reposted to the `datatalks.yellow_taxi_rides.low_amount` topic.
        * Otherwise, the message is reposted to `datatalks.yellow_taxi_rides.high_amount`.
    * You will need to run this script as `python branch_price.py worker` .

## Joins in Streams

Streams support the following Joins:
* ***Outer***
* ***Inner***
* ***Left***

Tables and streams can also be joined in different combinations:
* ***Stream to stream join*** - always ***windowed*** (you need to specify a certain timeframe).
* ***Table to table join*** - always NOT windowed.
* ***Stream to table join***.

You may find out more about how they behave [in this link](https://blog.codecentric.de/en/2017/02/crossing-streams-joins-apache-kafka/).

The main difference is that joins between streams are _windowed_ ([see below](#windowing)), which means that the joins happen between the "temporal state" of the window, whereas joins between tables aren't windowed and thus happen on the actual contents of the tables.

## Timestamps (Time Concept)

So far we have covered the key and value attributes of a Kafka message but we have not covered the timestamp.

Every event has an associated notion of time. Kafka Streams bases joins and windows on these notions. We actually have multiple timestamps available depending on our use case:
* ***Event time*** (extending `TimestampExtractor`): timestamp built into the message which we can access and recover.
* ***Processing time***: timestamp in which the message is processed by the stream processor.
* ***Ingestion time***: timestamp in which the message was ingested into its Kafka broker.

## Windowing

In Kafka Streams, ***windows*** refer to a time reference in which a series of events happen.

There are 2 main kinds of windows:

* ***Time-based windows***
    * ***Fixed/tumbling***: windows have a predetermined size (in seconds or whichever time unit is adequate for the use case) and don't overlap - each window happens one after another.
    * ***Sliding***: windows have a predetermined size but there may be multiple "timelines" (or _slides_) happening at the same time. Windows for each slide have consecutive windows.
* ***Session-based windows***: windows are based on keys rather than absolute time. When a key is received, a _session window_ starts for that key and ends when needed. Multiple sessions may be open simultaneously.

This is very useful when we want to find out something like: 
- How many rides is the vendor selling per hour/minute/second

## Kafka Streams demo (2) - Windowing

Let's now see an example of windowing in action.

* `windowing.py` ([link](../streams/windowing.py)) is a very similar app to `stream_count_vendor_trips.py` but defines a ***tumbling window*** for the table.
    * The window will be of 1 minute in length.
    * When we run the app and check the window topic in Control Center, we will see that each key (one per window) has an attached time interval for the window it belongs to and the value will be the key for each received message during the window.
    * You will need to run this script as `python windowing.py worker` .


## Additional Streams features

Many of the following features are available in the official Streams library for the JVM but aren't available yet in alternative libraries such as Faust.

### Stream tasks and threading model

In Kafka Streams, each topic partition is handled by a ***task***. Tasks can be understood as a mechanism for Kafka to handle parallelism, regardless of the amount of computing ***threads*** available to the machine.

![tasks](images/06_05.jpeg)

Kafka also allows us to define the amount of threads to use. State is NOT shared within threads even if they run in a single instance; this allows us to treat threads within an instance as if they were threads in separate machines. Scalability is handled by the Kafka cluster.

Threading Model
- Configure number of threads
- Allows parallelizing in a single instance
- No state shared within threads
- Same as having multiple instance
- Scalability handled by Kafka cluster

![tasks](images/06_06.png)
??????
![tasks](images/06_07.png)

### Joins

In Kafka Streams, join topics should have the _same partition count_.

Remember that joins are based on keys, and partitions are assigned to instances. When doing realtime joins, identical keys between the 2 topics will be assigned to the same partition, as shown in the previous image.

If you're joining external topics and the partitions don't match, you may need to create new topics recreating the data and repartition these new topics as needed. In Spark this wouldn't be necessary.

In real time joins, keys are distributed accross partition via the following formula:
- Hash of ***Key***%(partition count)

### Global KTable

A ***global KTable*** is a KTable that acts like a _broadcast variable_. All partitions of a global KTable are stored in all Kafka instances.

The benefits of global KTables are more convenient and effective joins and not needing to co-partition data, but the drawbacks are increased local storage and network load. Ideally, global KTables should be reserved for smaller data.

### Interactive queries

Let's assume that you have a Kafka Streams app which captures events from Kafka and you also have another app which would benefit from querying the data of your Streams app. Normally, you'd use an external DB to write from your Streams app and the other apps would query the DB.

***Interactive queries*** is a feature that allows external apps to query your Streams app directly, without needing an external DB.

Assuming that you're running multiple instances of your Streams app, when an external app requests a key to the Streams app, the load balancer will fetch the key from the appropiate Streams app instance and return it to the external app. This can be achieved thanks to the _Interactive queries-RPC API_.
* `KafkaStreams#allMetadata()`
* `KafkaStreams#allMetadataForStore(String storeName)`
* `KafkaStreams#metadataForKey(String storeName, K key, Serializer<K> keySerializer)`
* `KafkaStreams#metadataForKey(String storeName, K key, StreamPartitioner<K, ?> partitiones)`

### Processing guarantees

Depending on your needs, you may specify the message ***processing guarantee***:
* At least once: messages will be read but the system will not check for duplicates.
* Exactly once: records are processed once, even if the producer sends duplicate records.

You can find more about processing guarantees and their applications [in this link](https://docs.confluent.io/platform/current/streams/concepts.html#:~:text=the%20Developer%20Guide.-,Processing%20Guarantees,and%20exactly%2Donce%20processing%20guarantees.&text=Records%20are%20never%20lost%20but,read%20and%20therefore%20re%2Dprocessed.).
