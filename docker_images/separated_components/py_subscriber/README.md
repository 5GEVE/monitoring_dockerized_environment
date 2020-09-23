# Kafka Python subscriber

Docker image with the logic needed to enable a Python subscriber for Kafka, listening to the port specified as argument.

## Build the image

```sh
$ docker build -t py_subscriber .
```

## Run the image

```sh
$ docker run --name <container_name> -it py_subscriber python3 subscriber.py <ip>:<port> <topic>
```

Where:

* **container_name:** name for the container to be deployed.
* **ip:** DCM IP address in the same network than the one used by this subscriber.
* **port:** port to which Kafka is listening in that network (e.g. 9093).
* **topic:** Kafka topic in which the subscriber will listen to.
