# Docker images

In this folder, you can find the Docker images that can be used in the Monitoring Dockerized environment.

## Structure of the repository

There are three main folders in this repository, in which you can find some useful README files to quickly check the content of each of them. The folders are the following:

* **[full_components](full_components):** contains the images related to full components from the 5G EVE Monitoring architecture (i.e. Data Collection Manager and Data Collection and Storage-Visualization components).
* **[microservices_scenario](microservices_scenario):** contains images related to the microservices scenario, in which the 5G EVE Monitoring Platform is decoupled in different microservices. This is a previous step before deploying the platform using serverless functions.
* **[separated_components](separated_components):** contains the images related to individual components of the 5G EVE Monitoring architecture, distinguishing between the building blocks that belong to each component (e.g. Kafka and ZooKeeper are individual components from the Data Collection Manager).
