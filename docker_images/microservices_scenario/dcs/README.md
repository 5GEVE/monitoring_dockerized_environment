# DCS Docker image

Docker image containing the DCS, which triggers the execution of other microservices placed on the DCS from the Monitoring platform of 5G EVE.

## Build the image

```sh
$ docker build -t dcs .
```

## Run the image

```sh
$ docker run --name <container_name> -p 8091:8091 -t -d dcs
```

Where:

* **container_name:** name for the container to be deployed.

## Configure the Container

Run the following command in the container:

```sh
$ docker exec -it <container_name> /bin/bash entrypoint.sh $dcs_dashboard_ip_port $logstash_pipeline_manager_ip_port $kafka_consumer_ip_port $elasticsearch_ip_port
```

Where:

* **dcs_dashboard_ip_port:** IP:port of the DCS Dashboard service (localhost:8080 by default, but must be changed with the final IP address used in the Kibana container).
* **logstash_pipeline_manager_ip_port:** IP:port of Logstash Pipeline Manager (localhost:8191 by default, but must be changed with the final IP address used in the Logstash Pipeline Manager container).
* **kafka_consumer_ip_port:** IP:port of Kafka Consumer (localhost:8291 by default, but must be changed with the final IP address used in the Kafka Consumer container).
* **elasticsearch_ip_port:** IP:port of Elasticsearch (localhost:9200 by default, but must be changed with the final IP address used in the Elasticsearch container).

## Checking the correct deployment of the service

By executing the following command, the correct deployment of the service can be checked. In case of not receiving a message, it means that everything went fine.

```sh
$ curl --location --request GET 'http://<container_ip>:8091'
```
