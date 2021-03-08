FROM ubuntu:xenial

# Install packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jre openjdk-8-jdk curl nano git iputils-ping apt-transport-https wget jq

# Set JAVA_HOME
RUN sed -i '/^JAVA_HOME.*/d' /etc/environment && echo JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd4 | tee -a /etc/environment > /dev/null

# Install ELK Stack
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
ADD https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.5.0-amd64.deb /tmp
RUN dpkg -i /tmp/elasticsearch-7.5.0-amd64.deb
RUN rm /tmp/*.deb

# Configure Elasticsearch - check security and if Elasticsearch password is needed
RUN sed -i -e "s/#network.host: 192.168.0.1/network.host: 0.0.0.0/" /etc/elasticsearch/elasticsearch.yml
RUN sed -i -e 's/#cluster.name: my-application/cluster.name: "dcs"/' /etc/elasticsearch/elasticsearch.yml
RUN echo "discovery.type: single-node" | tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
RUN echo "xpack.license.self_generated.type: basic" | tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
RUN echo "xpack.security.enabled: false" | tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
RUN echo "xpack.monitoring.collection.enabled: true" | tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null

# Entrypoint script
COPY files/entrypoint.sh /
RUN chmod +x entrypoint.sh
CMD /entrypoint.sh
