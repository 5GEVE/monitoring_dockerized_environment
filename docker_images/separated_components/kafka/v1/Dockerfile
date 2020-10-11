FROM ubuntu:xenial

# Install packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk curl nano iputils-ping

# Download Kafka
ARG kafka_version=2.5.0
ADD https://downloads.apache.org/kafka/$kafka_version/kafka_2.12-$kafka_version.tgz /opt
RUN tar -xzf /opt/kafka_2.12-$kafka_version.tgz -C /opt && mv /opt/kafka_2.12-$kafka_version /opt/kafka
RUN rm /opt/kafka_2.12-$kafka_version.tgz

# Declare environment variables
ENV listener_ip_addresses=PLAINTEXT://0.0.0.0:9092
ENV adv_listener_ip_addresses=PLAINTEXT://127.0.0.1:9092
ENV broker_id=0
ENV zookeeper_ip_address=127.0.0.1
ENV listener_security_protocol_map=PLAINTEXT:PLAINTEXT
ENV inter_broker_listener_name=PLAINTEXT
ENV rack_name=kafka
ENV network_commands=false

# Modify /opt/kafka/config/server.properties (lines without environment variables)
RUN echo 'delete.topic.enable=true' | tee -a /opt/kafka/config/server.properties > /dev/null
RUN echo 'auto.create.topics.enable=false' | tee -a /opt/kafka/config/server.properties > /dev/null
RUN echo 'replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector' | tee -a /opt/kafka/config/server.properties > /dev/null
RUN sed -i -e "s/offsets.topic.replication.factor=1/offsets.topic.replication.factor=2/" /opt/kafka/config/server.properties

# Entrypoint script
COPY files/entrypoint.sh /
RUN chmod +x entrypoint.sh
ENTRYPOINT /bin/bash entrypoint.sh
