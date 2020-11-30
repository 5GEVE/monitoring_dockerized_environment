# Fetch Kafka Topic image

Docker image containing the Fetch Kafka Topic, microservice that allows to check if a topic exists or not in Kafka.

## Build the image

```sh
$ docker build -t fetch_kafka_topic .
```

## Run the image

```sh
$ docker run --name <container_name> -p 8390:8390 -t -d fetch_kafka_topic
```

Where:

* **container_name:** name for the container to be deployed.

## Configure the Container

Run the following commands in the container:

```sh
$ docker exec -it <container_name> /bin/bash update_hosts.sh $ip $hostname
```

Where:

* **ip:** IP address to assign a hostname.
* **hostname:** hostname assigned, to be used in the following command.

```sh
$ docker exec -it <container_name> /bin/bash entrypoint.sh $kafka_ip_port
```

Where:

* **kafka_ip_port:** IP:port of Kafka (localhost:9092 by default, but must be changed with the final IP address used in the Kafka container).

## Checking the correct deployment of the service

By executing the following command, the correct deployment of the service can be checked. In case of not receiving a message, it means that everything went fine.

```sh
$ curl --location --request GET 'http://<container_ip>:8390'
```
