# Logstash Docker image

Docker image containing Logstash, from the ELK Stack. It also contains the DCS-DV handler, as it interacts with Logstash files, and PostgreSQL to save the names of the pipelines created.

## Build the image

```sh
$ docker build -t logstash .
```

## Run the image

```sh
$ docker run --name <container_name> -p 28091:8091 -t -d logstash
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
$ docker exec -it <container_name> /bin/bash entrypoint.sh $elasticsearch_ip_address $dcm_ip_address $elasticsearch_hosts $kibana_ip_address
```

* **elasticsearch_ip_address:** IP address of Elasticsearch (localhost by default, but must be changed with the final IP address used in the Elasticsearch container).
* **dcm_ip_address:** IP address of DCM (localhost by default, but must be changed with the final IP address used in the DCM container).
* **elasticsearch_hosts:** hosts that belongs to the Elasticsearch cluster, written as a list (e.g. \"host1\", \"host2\"...).
* **kibana_ip_address:** IP address of Kibana (localhost by default, but must be changed with the final IP address used in the Kibana container).

## Checking the correct deployment of the DCS-DV

By executing the following command, the correct deployment of the DCS-DV can be checked. In case of not receiving a message, it means that everything went fine.

```sh
$ curl --location --request GET 'http://<container_ip>:28091'
```
