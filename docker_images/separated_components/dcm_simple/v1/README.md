# DCM simple Docker image

Docker image with the simplified version of the DCM, only including the Kafka broker to be placed in the Interworking Layer and the Python logic that handles the Kafka topics.

## Build the image

```sh
$ docker build -t dcm_simple .
```

## Run the image

```sh
$ docker run --name <container_name> -p 28090:8090 --env-file=env_file -d dcm_simple
```

Where:

* **container_name:** name for the container to be deployed.

And, in the env_file, the following parameter can be modified:

* **dcm_ip_address:** IP address of the DCM, to publish data in signalling topics (localhost by default, but must be changed with the final IP address used in the DCM handler container).
* **zookeeper_ip_address:** IP address of ZooKeeper (localhost by default, but must be changed with the final IP address used in the ZooKeeper container).
* **kafka_port:** Kafka port to be used to publish data in the signalling topics (9092 by default).
* **listener_ip_addresses:** IP addresses in which Kafka is listening to (0.0.0.0 by default). A listener must be included for each network in which there can be clients connected to Kafka.
* **adv_listener_ip_addresses:** IP addresses to be advertised by Kafka for the different Kafka clients connected to the broker. A listener must be included for each network in which there can be clients connected to Kafka.
* **broker_id:** value of the brokerId (0 by default).
* **listener_security_protocol_map:** a mapping of the alias assigned to each security protocol used for each listener.
* **inter_broker_listener_name:** security protocol used in the inter-broker listener.
* **rack_name:** name of the Kafka broker to be used by consumers that handles the client.rack attribute.
* **network_commands:** commands to be applied to correctly configure the network (leave it to "false" if you do not need this kind of commands).

## Checking the correct deployment of the DCM handler

By executing the following command, the correct deployment of the DCM can be checked. In case of not receiving a message, it means that everything went fine.

```sh
$ curl --location --request GET 'http://127.0.0.1:28090'
```

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
