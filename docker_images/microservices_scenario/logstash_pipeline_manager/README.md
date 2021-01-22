# Logstash and pipeline manager Docker image

Docker image containing Logstash, from the ELK Stack. It also contains the Logstash pipeline manager, as it interacts with Logstash files.

## Build the image

```sh
$ docker build -t logstash_pipeline_manager:vNoRack .
```

## Run the image

```sh
$ docker run --name <container_name> -p 8191:8191 -t -d logstash_pipeline_manager:vNoRack
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
$ docker exec -it <container_name> /bin/bash entrypoint.sh $elasticsearch_hosts $kafka_ip_port $elasticsearch_ip_port
```

* **elasticsearch_hosts:** hosts that belongs to the Elasticsearch cluster, written as a list (e.g. \"host1\", \"host2\"...).
* **kafka_ip_port:** IP:port of Kafka (localhost:9092 by default, but must be changed with the final IP address used in the Kafka container).
* **elasticsearch_ip_port:** IP:port of Elasticsearch (localhost:9200 by default, but must be changed with the final IP address used in the Elasticsearch container).

## Checking the correct deployment of the service

By executing the following command, the correct deployment of the service can be checked. In case of not receiving a message, it means that everything went fine.

```sh
$ curl --location --request GET 'http://<container_ip>:8191'
```
