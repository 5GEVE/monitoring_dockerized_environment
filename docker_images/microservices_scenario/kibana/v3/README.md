# Kibana Docker image

Docker image containing Kibana, from the ELK Stack. It also contains the dashboards' handler, as it interacts with Kibana, and PostgreSQL to save the dashboards' data.

## Build the image

```sh
$ docker build -t kibana:v3 .
```

## Run the image

```sh
$ docker run --name <container_name> -p 5601:5601 -p 8080:8080 -t -d kibana:v3
```

Where:

* **container_name:** name for the container to be deployed.

## Configure the Container

Run the following command in the container:

```sh
$ docker exec -it <container_name> /bin/bash entrypoint.sh $kibana_ip_address $elasticsearch_hosts 
```

* **kibana_ip_address:** IP address of Kibana (localhost by default, but must be changed with the final IP address used in the Kibana container).
* **elasticsearch_hosts:** hosts that belongs to the Elasticsearch cluster, written as a list (e.g. \"host1\", \"host2\"...).
