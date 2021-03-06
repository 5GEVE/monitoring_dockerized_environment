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
ADD https://downloads.apache.org/kafka/$kafka_version/kafka_2.12-$kafka_version.tgz /opt
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
