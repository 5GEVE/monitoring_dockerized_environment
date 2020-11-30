# Kafka Consumer image

Docker image containing the Kafka Consumer, microservice that enables a Kafka consumer waiting for the first message on a given topic to create the corresponding dashboard.

## Build the image

```sh
$ docker build -t kafka_consumer .
```

## Run the image

```sh
$ docker run --name <container_name> -p 8291:8291 -t -d kafka_consumer
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
$ docker exec -it <container_name> /bin/bash entrypoint.sh $dcs_dashboard_ip_port $kafka_ip_port
```

Where:

* **dcs_dashboard_ip_port:** IP:port of the DCS Dashboard service (localhost:8080 by default, but must be changed with the final IP address used in the Kibana container).
* **kafka_ip_port:** IP:port of Kafka (localhost:9092 by default, but must be changed with the final IP address used in the Kafka container).

## Checking the correct deployment of the service

By executing the following command, the correct deployment of the service can be checked. In case of not receiving a message, it means that everything went fine.

```sh
$ curl --location --request GET 'http://<container_ip>:8291'
```
