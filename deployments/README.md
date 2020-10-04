# Deployments

This folder contains some testing scenarios to check the correct behaviour of the Monitoring platform in different deployments.

## Structure of the repository

Each folder corresponds to a specific deployment of the Dockerized environment.

* **[1_complete_dcm_with_subscriber_and_publisher](1_complete_dcm_with_subscriber_and_publisher):** contains the instructions to be followed to deploy the full DCM component with a subscriber and a publisher.
* **[2_uncoupled_dcm_with_subscriber_and_publisher](2_uncoupled_dcm_with_subscriber_and_publisher):** contains the instructions to be followed to deploy the uncoupled DCM component with a subscriber and a publisher.
* **[3_two_kafka_brokers_with_subscriber_and_publisher](3_two_kafka_brokers_with_subscriber_and_publisher):** contains the instructions to be followed to deploy a multi-broker scenario with two Kafka brokers, a subscriber and a publisher.
* **[4_two_kafka_brokers_with_dcs_dv_and_publisher](4_two_kafka_brokers_with_dcs_dv_and_publisher):** contains the instructions to be followed to deploy a multi-broker scenario with two Kafka brokers, a DCS-DV complete instance and a publisher.
