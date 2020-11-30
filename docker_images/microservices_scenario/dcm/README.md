# DCM Docker image

Docker image containing the DCM, which triggers the execution of other microservices placed on the DCM from the Monitoring platform of 5G EVE.

## Build the image

```sh
$ docker build -t dcm .
```

## Run the image

```sh
$ docker run --name <container_name> -p 8090:8090 -t -d dcm
```

Where:

* **container_name:** name for the container to be deployed.

## Configure the Container

Run the following command in the container:

```sh
$ docker exec -it <container_name> /bin/bash entrypoint.sh $dcs_rest_client_ip_port $create_kafka_topic_ip_port $delete_kafka_topic_ip_port $fetch_kafka_topic_ip_port
```

Where:

* **dcs_rest_client_ip_port:** IP:port of the DCS service (localhost:8091 by default, but must be changed with the final IP address used in the DCS container).
* **create_kafka_topic_ip_port:** IP:port of Create Kafka Topic (localhost:8190 by default, but must be changed with the final IP address used in the Create Kafka Topic container).
* **delete_kafka_topic_ip_port:** IP:port of Delete Kafka Topic (localhost:8290 by default, but must be changed with the final IP address used in the Delete Kafka Topic container).
* **fetch_kafka_topic_ip_port:** IP:port of Fetch Kafka Topic (localhost:8390 by default, but must be changed with the final IP address used in the Fetch Kafka Topic container).

## Checking the correct deployment of the service

By executing the following command, the correct deployment of the service can be checked. In case of not receiving a message, it means that everything went fine.

```sh
$ curl --location --request GET 'http://<container_ip>:8090'
```
