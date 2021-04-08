FROM ubuntu:xenial

# Install packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk curl nano iputils-ping

# Download Kafka
ARG kafka_version=2.5.0
ADD https://archive.apache.org/dist/kafka/$kafka_version/kafka_2.12-$kafka_version.tgz /opt
RUN tar -xzf /opt/kafka_2.12-$kafka_version.tgz -C /opt && mv /opt/kafka_2.12-$kafka_version /opt/kafka
RUN rm /opt/kafka_2.12-$kafka_version.tgz

# Entrypoint script
COPY files/entrypoint.sh /
RUN chmod +x entrypoint.sh
ENTRYPOINT /bin/bash entrypoint.sh
