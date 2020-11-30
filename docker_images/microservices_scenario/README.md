# Docker images related to the microservices scenario

In this folder, you can find the Docker images related to the microservices scenario, in which the 5G EVE Monitoring Platform is decoupled in different microservices. This is a previous step before deploying the platform using serverless functions.

## Structure of the repository

Each folder contains a specific Docker image for a specific building block of the 5G EVE Monitoring architecture. The folders are the following:

* **[complex_publisher](complex_publisher):** it contains the Docker image related to a Kafka Python publisher installed in an Ubuntu container.
* **[complex_subscriber](complex_subscriber):** it contains the Docker image related to a Kafka Python subscriber installed in an Ubuntu container.
* **[create_kafka_topic](create_kafka_topic):** it contains the Docker image related to the Create Kafka Topic microservice.
* **[dcm](dcm):** it contains the Docker image related to the DCM microservice.
* **[dcs](dcs):** it contains the Docker image related to the DCS microservice.
* **[delete_kafka_topic](delete_kafka_topic):** it contains the Docker image related to the Delete Kafka Topic microservice.
* **[elasticsearch](elasticsearch):** it contains the Docker image related to Elasticsearch.
* **[fetch_kafka_topic](fetch_kafka_topic):** it contains the Docker image related to the Fetch Kafka Topic microservice.
* **[kafka](kafka):** it contains the Docker image related to Kafka, as used in 5G EVE. It can emulate the Kafka broker to be placed in each site facility.
* **[kafka_consumer](kafka_consumer):** it contains the Docker image related to the Kafka Consumer microservice.
* **[kibana](kibana):** it contains the Docker image related to Kibana, also including the Java logic that manages the dashboards.
* **[logstash_pipeline_manager](logstash_pipeline_manager):** it contains the Docker image related to Logstash, also including a Python logic managing the pipeline's configuration.
* **[sangrenel_publisher](sangrenel_publisher):** it contains the Docker image related to Sangrenel.
* **[zookeeper](zookeeper):** it contains the Docker image related to ZooKeeper, as used in 5G EVE.
