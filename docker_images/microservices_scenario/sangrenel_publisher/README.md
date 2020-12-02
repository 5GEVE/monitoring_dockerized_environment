# Sangrenel publisher

Docker image with [Sangrenel](https://github.com/jamiealquiza/sangrenel) installed, to do performance tests with a Kafka cluster.

## Build the image

```sh
$ docker build -t sangrenel_publisher .
```

## Run the image

```sh
# Create the container and then execute the script
$ docker run --name <container_name> -t -d sangrenel_publisher
$ docker exec -it <container_name> bin/sangrenel -brokers <broker_ip_and_port> -interval <interval> -message-batch-size <batch_size> -message-size <msg_size> -produce-rate <rate> -topic <topic> -writers-per-worker <writers>

# All in one single command
$ docker run --name <container_name> -it sangrenel_publisher bin/sangrenel -brokers <broker_ip_and_port> -interval <interval> -message-batch-size <batch_size> -message-size <msg_size> -produce-rate <rate> -topic <topic> -writers-per-worker <writers>
```

Where:

* **container_name:** name for the container to be deployed.
* **broker_ip_and_port:** IP:port to reach the Kafka broker from which you want to consume data (default "localhost:9092").
* **interval:** statistics output interval (seconds) (default 5).
* **batch_size:** messages per batch (default 500).
* **msg_size:** message size (bytes) (default 300).
* **rate:** global write rate limit (messages/sec) (default 100000000)
* **topic:** topic to consume from.
* **writers:** number of writer (Kafka producer) goroutines per worker (default 5).

For more information about Sangrenel and the parameters that can be defined, check its [Github](https://github.com/jamiealquiza/sangrenel) page.
