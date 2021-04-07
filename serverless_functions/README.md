# Serverless functions

The serverless functions to be used in the Kubernetes + DNS scenario can be found in this repository.

## Functions available

The functions that can be used are the following:

* **[create-kafka](create-kafka):** implements the Create Kafka Topic function.
* **[dcm](dcm):** implements the DCM function.
* **[dcs](dcs):** implements the DCS function.
* **[delete-kafka](delete-kafka):** implements the Delete Kafka Topic function.
* **[fetch-kafka](fetch-kafka):** implements the Fetch Kafka Topic function.
* **[kafka-consumer](kafka-consumer):** implements the Kafka Consumer function.

## How to deploy the functions

Execute the following commands:

```sh
$ faas-cli template pull https://github.com/openfaas-incubator/python-flask-template # In Tardis, this also worked: faas-cli template store pull python3-http
$ faas-cli build -f ./stack.yml
$ faas-cli deploy -f ./stack.yml # Use the gateway IP obtained from this command: kubectl get svc -n openfaas gateway-external -o wide
```

## How to remove the functions

Execute the following commands:

```sh
$ faas-cli remove -f ./stack.yml
```
