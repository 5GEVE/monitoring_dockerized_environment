FROM ubuntu:xenial

# Install packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk python3 python3-pip curl locales nano git iputils-ping

# Build locales database
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

# Download Kafka
ARG kafka_version=2.5.0
ADD https://apache.brunneis.com/kafka/$kafka_version/kafka_2.12-$kafka_version.tgz /opt
RUN tar -xzf /opt/kafka_2.12-$kafka_version.tgz -C /opt && mv /opt/kafka_2.12-$kafka_version /opt/kafka
RUN rm /opt/kafka_2.12-$kafka_version.tgz

# Create /usr/bin/dcm directory
RUN mkdir -p /usr/bin/dcm/dcm-python
RUN chmod 755 /usr/bin/dcm/dcm-python
RUN chown root:root /usr/bin/dcm/dcm-python

# Download 5geve-wp3-dcm-handler project and move it to /usr/bin/dcm/dcm-python directory
RUN mkdir -p /tmp/5geve-wp3-dcm-handler
RUN git clone -b dev-dockerized https://github.com/5GEVE/5geve-wp3-dcm-handler.git /tmp/5geve-wp3-dcm-handler
RUN mv /tmp/5geve-wp3-dcm-handler/* /usr/bin/dcm/dcm-python && rm -r /tmp/5geve-wp3-dcm-handler

# Install Python libraries for DCM
RUN export LC_ALL="en_US.UTF-8"
RUN export LC_CTYPE="en_US.UTF-8"
RUN pip3 install -r /usr/bin/dcm/dcm-python/requirements.txt
RUN pip3 install requests
RUN pip3 install flask-swagger

# Declare environment variables
ENV dcm_ip_address=127.0.0.1
ENV zookeeper_ip_address=127.0.0.1
ENV kafka_port=9092
ENV listener_ip_addresses=PLAINTEXT://0.0.0.0:9092
ENV adv_listener_ip_addresses=PLAINTEXT://127.0.0.1:9092
ENV broker_id=0
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
