# Deployments

This folder contains some testing scenarios to check the correct behaviour of the Monitoring platform in different deployments.

## Structure of the repository

Each folder corresponds to a specific deployment of the Dockerized environment.

* **[0_preliminary_monitoring_dockerized_env](0_preliminary_monitoring_dockerized_env):** contains a reference to the previous Monitoring Dockerized environment built to test the features of the platform.
* **[1_complete_dcm_with_subscriber_and_publisher](1_complete_dcm_with_subscriber_and_publisher):** contains the instructions to be followed to deploy the full DCM component with a subscriber and a publisher.
* **[2_uncoupled_dcm_with_subscriber_and_publisher](2_uncoupled_dcm_with_subscriber_and_publisher):** contains the instructions to be followed to deploy the uncoupled DCM component with a subscriber and a publisher.
* **[3_two_kafka_brokers_with_subscriber_and_publisher](3_two_kafka_brokers_with_subscriber_and_publisher):** contains the instructions to be followed to deploy a multi-broker scenario with two Kafka brokers, a subscriber and a publisher.
* **[4_two_kafka_brokers_with_dcs_dv_and_publisher](4_two_kafka_brokers_with_dcs_dv_and_publisher):** contains the instructions to be followed to deploy a multi-broker scenario with two Kafka brokers, a DCS-DV complete instance and a publisher.
* **[5_two_kafka_brokers_with_subscriber_and_publisher_kubernetes](5_two_kafka_brokers_with_subscriber_and_publisher_kubernetes):** same than scenario 3, but using Kubernetes.
* **[6_two_kafka_brokers_with_uncoupled_dcs_dv_and_publisher_kubernetes](6_two_kafka_brokers_with_uncoupled_dcs_dv_and_publisher_kubernetes):** this scenario, based on Kubernetes, contains two Kafka brokers and the uncoupled version of the DCS-DV. Two type of publishers, based on Sangrenel and Python, are also used.
* **[7_microservices_deployment_kubernetes](7_microservices_deployment_kubernetes):** this scenario, based on Kubernetes, contains the Monitoring platform based on microservices, which is the previous step before achieving the integration of serverless functions.
