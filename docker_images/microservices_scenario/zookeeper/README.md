# ZooKeeper Docker image

Docker image containing ZooKeeper, acting as the coordinator for the Kafka multi-broker configuration.

## Build the image

```sh
$ docker build -t zookeeper .
```

## Run the image

```sh
$ docker run --name <container_name> -d zookeeper
```

Where:

* **container_name:** name for the container to be deployed.

## Some ZooKeeper commands to have in mind

As a reminder, the following ZooKeeper commands can be used within the container to test the correct configuration and behaviour of ZooKeeper and the Kafka broker:

```sh
# Obtain information about a topic already created in the system
/opt/kafka/bin/kafka-topics.sh --describe --topic <topic> --zookeeper <zookeeper_ip_address>:2181

# Obtain the Kafka brokers connected to ZooKeeper
/opt/kafka/bin/zookeeper-shell.sh <zookeeper_ip_address>:2181 ls /brokers/ids

# Obtain the information related to a Kafka broker
/opt/kafka/bin/zookeeper-shell.sh <zookeeper_ip_address>:2181 get /brokers/ids/<broker_id>
```
