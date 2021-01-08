FROM ubuntu:xenial

# Install packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk curl nano iputils-ping

# Download Kafka
ARG kafka_version=2.5.0
ADD https://downloads.apache.org/kafka/$kafka_version/kafka_2.12-$kafka_version.tgz /opt
RUN tar -xzf /opt/kafka_2.12-$kafka_version.tgz -C /opt && mv /opt/kafka_2.12-$kafka_version /opt/kafka
RUN rm /opt/kafka_2.12-$kafka_version.tgz

# Modify /opt/kafka/config/server.properties (lines without environment variables)
RUN echo 'delete.topic.enable=true' | tee -a /opt/kafka/config/server.properties > /dev/null
RUN echo 'auto.create.topics.enable=false' | tee -a /opt/kafka/config/server.properties > /dev/null
RUN echo 'replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector' | tee -a /opt/kafka/config/server.properties > /dev/null
RUN echo 'listener.security.protocol.map=PLAINTEXT:PLAINTEXT' | tee -a /opt/kafka/config/server.properties > /dev/null
RUN echo 'inter.broker.listener.name=PLAINTEXT' | tee -a /opt/kafka/config/server.properties > /dev/null
RUN sed -i -e "s/offsets.topic.replication.factor=1/offsets.topic.replication.factor=2/" /opt/kafka/config/server.properties

# Entrypoint script
COPY files/update_hosts.sh /
RUN chmod +x update_hosts.sh
COPY files/entrypoint.sh /
RUN chmod +x entrypoint.sh
CMD ["/entrypoint.sh", "PLAINTEXT://0.0.0.0:9092", "PLAINTEXT://dcm:9092", "1", "zookeeper", "dcm"]
