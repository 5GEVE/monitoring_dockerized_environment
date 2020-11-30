# Kafka Python complex subscriber

Docker image with the logic needed to enable a Python subscriber for Kafka, listening to the port specified as argument. This is a complex subscriber because it can be deployed without needing to execute the Python script, for troubleshooting purposes (e.g. do connectivity tests and so on).

## Build the image

```sh
$ docker build -t complex_subscriber .
```

## Run the image

```sh
# Create the container and then execute the script
$ docker run --name <container_name> -d complex_subscriber
$ docker exec -it <container_name> python3 subscriber.py <ip>:<port> <topic>

# All in one single command
$ docker run --name <container_name> -it complex_subscriber python3 subscriber.py <ip>:<port> <topic>
```

Where:

* **container_name:** name for the container to be deployed.
* **ip:** DCM IP address in the same network than the one used by this subscriber.
* **port:** port to which Kafka is listening in that network (e.g. 9093).
* **topic:** Kafka topic in which the subscriber will listen to.
