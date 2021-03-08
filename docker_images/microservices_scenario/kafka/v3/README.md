# Kafka Docker image

Docker image containing Kafka, configured to be used in the 5G EVE Monitoring architecture with multi-cluster configuration. It emulates the Kafka broker to be placed in each site facility.

## Build the image

```sh
$ docker build -t kafka:v3.
```

## Run the image

```sh
$ docker run --name <container_name> -t -d kafka:v3
```

Where:

* **container_name:** name for the container to be deployed.

## Configure the Container

Edit the Dockerfile and rebuild the image.

Check this line:

```
CMD ["/entrypoint.sh", "PLAINTEXT://0.0.0.0:9092", "PLAINTEXT://kafka:9092", "0", "zookeeper", "kafka"]
```

The script parameters are (in order):

* **listener_ip_addresses:** IP addresses in which Kafka is listening to (0.0.0.0 by default). A listener must be included for each network in which there can be clients connected to Kafka.
* **adv_listener_ip_addresses:** IP addresses to be advertised by Kafka for the different Kafka clients connected to the broker. A listener must be included for each network in which there can be clients connected to Kafka.
* **broker_id:** value of the brokerId (0 by default).
* **zookeeper_ip_address:** IP address of ZooKeeper.
* **rack_name:** name of the Kafka broker to be used by consumers that handles the client.rack attribute.

## Some Kafka commands to have in mind

As a reminder, the following Kafka commands can be used within the container to test the correct configuration and behaviour of Kafka:

```sh
# List the topics available in the Kafka broker
$ /opt/kafka/bin/kafka-topics.sh --list --zookeeper <zookeeper_ip_address>:2181

# Create a topic called <topic>, with one partition and without replication
$ /opt/kafka/bin/kafka-topics.sh --create --replication-factor 1 --zookeeper <zookeeper_ip_address>:2181 --topic <topic> --partitions 1

# Create a topic called <topic>, manually configuring the number of partitions and replication with <replica_assignment> (e.g., if we have two brokers, whose id are 1 and 4, and we want one partition with replication between the two brokers, where the broker 4 is the leader and the broker 1 is the follower, <replica_assignment>=4,1)
$ /opt/kafka/bin/kafka-topics.sh --create --zookeeper <zookeeper_ip_address>:2181 --topic <topic> --replica-assignment <replica_assignment>

# Start consuming from the topic called <topic>
$ /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic <topic>  --from-beginning

# Start consuming from the topic called <topic>, also indicating the broker from which the consumer must read, as defined in the broker.rack property in Kafka. Remember that the broker should have a replica of the topic partition to do this operation
$ /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic <topic> --consumer-property client.rack=<rack> --from-beginning

# Start publishing in the topic called <topic>. An interactive session will be opened then, in which you can write some messages and push Enter to send them to Kafka
$ /opt/kafka/bin/kafka-console-producer.sh --topic <topic> --bootstrap-server 127.0.0.1:9092

# Delete a set of topics, defined in a comma-separated list
$ /opt/kafka/bin/kafka-topics.sh --delete --zookeeper <zookeeper_ip_address>:2181 --topic <topic_1>,...,<topic_N>
```
