# Kafka Python publisher

Docker image with the logic needed to enable a Python publisher for Kafka, publishing the data in the port specified as argument.

## Build the image

```sh
$ docker build -t py_publisher .
```

## Run the image

```sh
$ docker run --name <container_name> -it py_publisher python3 publisher.py <ip>:<port> <topic> <n_metrics>
```

Where:

* **container_name:** name for the container to be deployed.
* **ip:** DCM IP address in the same network than the one used by this publisher.
* **port:** port to which Kafka is listening in that network (e.g. 9092).
* **topic:** Kafka topic in which the publisher will publish the data.
* **n_metrics:** Number of publish operations performed by this publisher.
