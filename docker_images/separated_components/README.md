# Docker images related to separated components

In this folder, you can find the Docker images related to separated components (i.e. building blocks) from the 5G EVE Monitoring platform.

## Structure of the repository

Each folder contains a specific Docker image for a specific building block of the 5G EVE Monitoring architecture. The folders are the following:

* **[complex_publisher](complex_publisher):** it contains the Docker image related to a Kafka Python publisher installed in an Ubuntu container.
* **[complex_subscriber](complex_subscriber):** it contains the Docker image related to a Kafka Python subscriber installed in an Ubuntu container.
* **[dcm_simple](dcm_simple):** it contains the Docker image related to the DCM, including Kafka and the DCM handler that manages the Kafka topics.
* **[kafka](kafka):** it contains the Docker image related to Kafka, as used in 5G EVE. It can emulate the Kafka broker to be placed in each site facility.
* **[nodejs_subscriber](nodejs_subscriber):** it contains the Docker image related to a Kafka NodeJS subscriber. It also calculates the publication latency.
* **[py_publisher](py_publisher):** it contains the Docker image related to a Kafka Python publisher.
* **[py_subscriber](py_subscriber):** it contains the Docker image related to a Kafka Python subscriber.
* **[sangrenel_publisher](sangrenel_publisher):** it contains the Docker image related to Sangrenel.
* **[zookeeper](zookeeper):** it contains the Docker image related to ZooKeeper, as used in 5G EVE.
