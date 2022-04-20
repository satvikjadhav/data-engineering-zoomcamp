# Kafka Configuration
	Topics to talk about
	- Configuration Terms
	- Configuring Producer, Consumer, and Topics
	- Producing dummy data to Kafka Topic
	- Consuming dummy data from Kafka Topic
	- How partitioning plays a role in scalability
	- How consumer group can scale across different partitions

## Topic configurations

* `retention.ms`: due to storage space limitations, messages can't be kept indefinitely. This setting specifies the amount of time (in milliseconds) that a specific topic log will be available before being deleted.
* `cleanup.policy`: when the `retention.ms` time is up, we may choose to `delete` or `compact` a topic log.
    * ***Compaction*** does not happen instantly; it's a batch job that takes time.
    * ***Compaction***: If we have Key K1 at time 0 and Key K2 at time 10, the last key will be persistent. And the same keys before that will be deleted or compacted.
    * ***Compaction*** is a background job and is not real time. It happens in batch mode, sequentially. 
* `partition`: number of partitions.
    * The higher the amount of partitions, the more resources Kafka requires to handle them. Remember that partitions will be replicated across brokers; if a broker dies we could easily overload the cluster.
    * Partition count really depends on how our consumers are behaving with the data, how much data we have, etc.
* `replication`: replication factor; number of times a partition will be replicated.

## Consumer configurations

* `offset`: sequence of message IDs which have been read by the consumer.
* `consumer.group.id`: ID for the consumer group. All consumers belonging to the same group contain the same `consumer.group.id`.
* `auto_offset_reset`: when a consumer subscribes to a pre-existing topic for the first time, Kafka needs to figure out which messages to send to the consumer.
    * If `auto_offset_reset` is set to `earliest`, all of the existing messages in the topic log will be sent to the consumer.
    * If `auto_offset_reset` is set to `latest`, existing old messages will be ignored and only new messages will be sent to the consumer.

## Producer configurations

* `acks`: behaviour policy for handling acknowledgement signals. It may be set to `0`, `1` or `all`.
    * `0`: "fire and forget". The producer will not wait for the leader or replica brokers to write messages to disk.
        * Fastest policy for the producer. Useful for time-sensitive applications which are not affected by missing a couple of messages every so often, such as log messages or monitoring messages.
    * `1`: the producer waits for the leader broker to write the messaage to disk.
        * If the message is processed by the leader broker but the broker inmediately dies and the message has not been replicated, the message is lost.
    * `all`: the producer waits for the leader and all replica brokers to write the message to disk.
        * Safest but slowest policy. Useful for data-sensitive applications which cannot afford to lose messages, but speed will have to be taken into account.

# Kafka Install and Demonstration

## Installing Kafka

_[Video source](https://www.youtube.com/watch?v=Erf1-d1nyMY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=58)_

Install instructions for Kafka can be found in [the official website](https://kafka.apache.org/quickstart#quickstart_kafkaconnect).

Due to the complexity of managing a manual Kafka install, a docker-compose script is provided [in this link](../docker-compose.yml). The Docker images are provided by [Confluent](https://www.confluent.io/), a Kafka tool vendor. The script defines the following services:

* **[`zookeeper`](https://zookeeper.apache.org/)**: a centralized service for maintaining configuration info. Kafka uses it for maintaining metadata knowledge such as topic partitions, etc.
    * Zookeeper is being phased out as a dependency, but for easier deployment we will use it in the lesson.
* **`broker`**: the main service. A plethora of environment variables are provided for easier configuration.
    * The image for this service packages both Kafka and [Confluent Server](https://docs.confluent.io/platform/current/installation/migrate-confluent-server.html), a set of commercial components for Kafka.
* **`kafka-tools`**: a set of additional Kafka tools provided by [Confluent Community](https://www.confluent.io/community/#:~:text=Confluent%20proudly%20supports%20the%20community,Kafka%C2%AE%EF%B8%8F%2C%20and%20its%20ecosystems.). We will make use of this service later in the lesson.
* **`schema-registry`**: provides a serving layer for metadata. We will make use of this service later in the lesson. 
* **`control-center`**: a web-based Kafka GUI.
    * Kafka can be entirely used with command-line tools, but the GUI helps us visualize things.

Download the script to your work directory and start the deployment with `docker-compose up` . It may take several minutes to deploy on the first run. Check the status of the deployment with `docker ps` . Once the deployment is complete, access the control center GUI by browsing to `localhost:9021` .

## Demo - Setting up a producer and consumer

We will now create a demo of a Kafka system with a producer and a consumer and see how messages are created and consumed.

1. In the Control Center GUI, select the `Cluster 1` cluster and in the topic section, create a new `demo_1` topic with 2 partitions and default settings.
2. Copy the [`requirements.txt`](../requirements.txt) to your work folder and [create a Python virtual environment](https://gist.github.com/ziritrion/8024025672ea92b8bdeb320d6015aa0d). You will need to run all the following scripts in this environment.
3. Copy the [`producer.py`](../producer.py) script to your work folder. Edit it and make sure that the line `producer.send('demo_1', value=data)` (it should be line 12 on an unmodified file) is set to `demo_1`. Run the script and leave it running in a terminal.
    * This script registers to Kafka as a producer and sends a message each second until it sends 1000 messages.
    * With the script running, you should be able to see the messages in the Messages tab of the `demo_1` topic window in Control Center.
4. Copy the [`consumer.py`](../consumer.py) script to your work folder. Edit it and make sure that the first argument of `consumer = KafkaConsumer()` is `'demo_1',` (in an unmodified script this should be in line 6) and the `group_id` value should be `'consumer.group.id.demo.1'`
    * This script registers to Kafka as a consumer and continuously reads messages from the topic, one message each second.
5. Run the `consumer.py` script on a separate terminal from `producer.py`. You should see the consumer read the messages in sequential order. Kill the consumer and run it again to see how itaa resumes from the last read message.
6. With the `consumer.py` running, modify the script and change `group_id` to `'consumer.group.id.demo.2'`. Run the script on a separate terminal; you should now see how it consumes all messages starting from the beginning because `auto_offset_reset` is set to `earliest` and we now have 2 separate consumer groups accessing the same topic.
7. On yet another terminal, run the `consumer.py` script again. The consumer group `'consumer.group.id.demo.2'` should now have 2 consumers. If you check the terminals, you should now see how each consumer receives separate messages because the second consumer has been assigned a partition, so each consumer receives the messages for their partitions only.
8. Finally, run a 3rd consumer. You should see no activity for this consumer because the topic only has 2 partitions, so no partitions can be assigned to the idle consumer.

