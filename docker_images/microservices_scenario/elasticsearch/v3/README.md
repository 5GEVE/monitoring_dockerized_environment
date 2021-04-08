# Elasticsearch Docker image

Docker image containing Elasticsearch, ready to be deployed with Kubernetes.

## Build the image

```sh
$ docker build -t elasticsearch:v3 .
```

## Run the image

```sh
$ docker run --name <container_name> -t -d elasticsearch:v3
```

Where:

* **container_name:** name for the container to be deployed.

## Configure the Container

Run the following command in the container:

```sh
$ docker exec -it <container_name> /bin/bash entrypoint.sh
