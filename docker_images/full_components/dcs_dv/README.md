# DCS-DV Docker image

Docker image with the full logic of the Data Collection and Storage-Data Visualization (DCS-DV) component from 5G EVE, including the ELK Stack and the logic that interacts with that stack.

## Build the image

```sh
$ docker build -t dcs_dv .
```

## Run the image

```sh
$ docker run --name <container_name> -p 28091:8091 -p 5601:5601 --env-file=env_file -d dcs_dv
```

Where:

* **container_name:** name for the container to be deployed.

And, in the env_file, the following parameters can be modified:

* **kibana_ip_address:** IP address of Kibana (localhost by default, but must be changed with the final IP address used in the Kibana container).
* **elasticsearch_ip_address:** IP address of Elasticsearch (localhost by default, but must be changed with the final IP address used in the Elasticsearch container).
* **elasticsearch_hosts:** hosts that belongs to the Elasticsearch cluster, written as a list (e.g. \"host1\", \"host2\"...).
* **dcm_ip_address:** IP address of DCM (localhost by default, but must be changed with the final IP address used in the DCM container).
* **network_commands:** commands to be applied to correctly configure the network (leave it to "false" if you do not need this kind of commands).

## Checking the correct deployment of the DCS-DV

By executing the following command, the correct deployment of the DCS-DV can be checked. In case of not receiving a message, it means that everything went fine.

```sh
$ curl --location --request GET 'http://127.0.0.1:28091'
```
