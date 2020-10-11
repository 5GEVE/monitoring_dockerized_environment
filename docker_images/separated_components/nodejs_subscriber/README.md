# Kafka subscriber based on NodeJS

Docker image with the logic needed to enable a NodeJS subscriber for Kafka. NodeJS is used to implement the rackId property to select the node from which you want to consume data from.

This subscriber also calculates the publication latency (i.e. time spent between the data is published by the publisher and received by this subscriber).

## Build the image

```sh
$ docker build -t nodejs_subscriber .
```

## Run the image

```sh
# Create the container and then execute the script
$ docker run --name <container_name> -t -d nodejs_subscriber
$ docker exec -it <container_name> node /usr/src/app/subscriber.js <broker_ip_and_port> <rackId> <topic>

# All in one single command
$ docker run --name <container_name> -it nodejs_subscriber node /usr/src/app/subscriber.js <broker_ip_and_port> <rackId> <topic>
```

Where:

* **container_name:** name for the container to be deployed.
* **broker_ip_and_port:** IP:port to reach the Kafka broker from which you want to consume data.
* **rackId:** rackId value, related to the selected broker.
* **topic:** topic to consume from.
