FROM ubuntu:xenial

# Install packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jre openjdk-8-jdk python3 python3-pip curl locales nano git iputils-ping apt-transport-https wget nginx jq maven

# Build locales database
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

# Set JAVA_HOME
RUN sed -i '/^JAVA_HOME.*/d' /etc/environment && echo JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd4 | tee -a /etc/environment > /dev/null

# Install ELK Stack
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
ADD https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.5.0-amd64.deb /tmp
ADD https://artifacts.elastic.co/downloads/kibana/kibana-7.5.0-amd64.deb /tmp
ADD https://artifacts.elastic.co/downloads/logstash/logstash-7.9.1.deb /tmp
RUN dpkg -i /tmp/elasticsearch-7.5.0-amd64.deb
RUN dpkg -i /tmp/kibana-7.5.0-amd64.deb
RUN dpkg -i /tmp/logstash-7.9.1.deb
RUN rm /tmp/*.deb

# Create /usr/bin/dcs directory
RUN mkdir -p /usr/bin/dcs/dcs-python
RUN chmod 755 /usr/bin/dcs/dcs-python
RUN chown root:root /usr/bin/dcs/dcs-python

# Copy auxiliary scripts
COPY files/create_logstash_pipeline.sh /usr/bin/dcs/create_logstash_pipeline.sh
COPY files/delete_logstash_pipeline.sh /usr/bin/dcs/delete_logstash_pipeline.sh
COPY files/refresh_dashboard.sh /usr/bin/dcs/refresh_dashboard.sh
RUN chmod +x /usr/bin/dcs/create_logstash_pipeline.sh
RUN chmod +x /usr/bin/dcs/delete_logstash_pipeline.sh
RUN chmod +x /usr/bin/dcs/refresh_dashboard.sh

# Download 5geve-wp4-dcs-signalling-topic-handler and move it to /usr/bin/dcs/dcs-python directory
RUN mkdir -p /tmp/5geve-wp4-dcs-signalling-topic-handler
RUN git clone -b v0.1 https://github.com/5GEVE/5geve-wp4-dcs-signalling-topic-handler.git /tmp/5geve-wp4-dcs-signalling-topic-handler
RUN mv /tmp/5geve-wp4-dcs-signalling-topic-handler/* /usr/bin/dcs/dcs-python && rm -r /tmp/5geve-wp4-dcs-signalling-topic-handler

# Download 5geve-wp4-dcs-kibana-dashboards-handler and 5geve-wp4-dcs-kibana-dashboards-generator
RUN mkdir -p /tmp/5geve-wp4-dcs-kibana-dashboards-handler
RUN git clone -b v0.1 https://github.com/5GEVE/5geve-wp4-dcs-kibana-dashboards-handler.git /tmp/5geve-wp4-dcs-kibana-dashboards-handler
RUN mkdir -p /tmp/5geve-wp4-dcs-kibana-dashboards-handler/5geve-wp4-dcs-kibana-dashboards-generator
RUN git clone --recursive -b v0.1 https://github.com/5GEVE/5geve-wp4-dcs-kibana-dashboards-generator.git /tmp/5geve-wp4-dcs-kibana-dashboards-handler/5geve-wp4-dcs-kibana-dashboards-generator
RUN rm -rf /tmp/5geve-wp4-dcs-kibana-dashboards-handler/kibana-dashboards && mv /tmp/5geve-wp4-dcs-kibana-dashboards-handler/5geve-wp4-dcs-kibana-dashboards-generator /tmp/5geve-wp4-dcs-kibana-dashboards-handler/kibana-dashboards

# Configure Elasticsearch - check security and if Elasticsearch password is needed
RUN sed -i -e "s/#network.host: 192.168.0.1/network.host: 0.0.0.0/" /etc/elasticsearch/elasticsearch.yml
RUN sed -i -e 's/#cluster.name: my-application/cluster.name: "dcs"/' /etc/elasticsearch/elasticsearch.yml
RUN echo "discovery.type: single-node" | tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
RUN echo "xpack.license.self_generated.type: basic" | tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
RUN echo "xpack.security.enabled: false" | tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null
RUN echo "xpack.monitoring.collection.enabled: true" | tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null

# Configure Kibana
ENV kibana_ip_address=127.0.0.1
ENV elasticsearch_ip_address=127.0.0.1
ENV elasticsearch_hosts=\"http://127.0.0.1:9200\"
RUN sed -i -e "s/PASSWORD=/PASSWORD=changeme/" /usr/bin/dcs/refresh_dashboard.sh
RUN sed -i -e 's/#server.name: "your-hostname"/server.name: kibana/' /etc/kibana/kibana.yml
RUN sed -i -e 's/#elasticsearch.username: "kibana"/elasticsearch.username: elastic/' /etc/kibana/kibana.yml
RUN sed -i -e 's/#elasticsearch.password: "pass"/elasticsearch.password: changeme/' /etc/kibana/kibana.yml
RUN echo "xpack.security.enabled: false" | tee -a /etc/kibana/kibana.yml > /dev/null

# Configure Logstash
ENV dcm_ip_address=127.0.0.1
RUN rm /etc/logstash/pipelines.yml && touch /etc/logstash/pipelines.yml
RUN sed -i -e "s/PASSWORD=/PASSWORD=changeme/" /usr/bin/dcs/create_logstash_pipeline.sh
RUN sed -i -e "s/PASSWORD=/PASSWORD=changeme/" /usr/bin/dcs/delete_logstash_pipeline.sh
RUN sed -i -e 's/# http.host: "127.0.0.1"/http.host: "0.0.0.0"/' /etc/logstash/logstash.yml
RUN sed -i -e 's/# config.reload.automatic: false/config.reload.automatic: true/' /etc/logstash/logstash.yml
RUN sed -i -e 's/# config.reload.interval: 3s/config.reload.interval: 1s/' /etc/logstash/logstash.yml
RUN sed -i -e 's/#xpack.monitoring.enabled: false/xpack.monitoring.enabled: true/' /etc/logstash/logstash.yml
RUN sed -i -e 's/#xpack.monitoring.elasticsearch.username: logstash_system/xpack.monitoring.elasticsearch.username: elastic/' /etc/logstash/logstash.yml
RUN sed -i -e 's/#xpack.monitoring.elasticsearch.password: password/xpack.monitoring.elasticsearch.password: changeme/' /etc/logstash/logstash.yml

# Install and configure PostgreSQL
COPY files/script_db.sql /tmp
RUN apt-get install -y postgresql postgresql-contrib python3-psycopg2 sudo
#RUN /etc/init.d/postgresql start
#RUN sudo -u postgres createuser eve
#RUN sudo -u postgres createdb dashboards
#RUN sudo -u postgres createdb pipelines
#RUN sudo -u postgres psql -f /tmp/script_db.sql
# Test to access DB: sudo -u postgres psql eve -h 127.0.0.1 -d dashboards
COPY files/script_table.sql /tmp
#RUN sudo -u postgres psql -f /tmp/script_table.sql -d pipelines

# Install Python libraries for DCS
RUN export LC_ALL="en_US.UTF-8"
RUN export LC_CTYPE="en_US.UTF-8"
RUN pip3 install -r /usr/bin/dcs/dcs-python/requirements.txt
RUN pip3 install requests
RUN pip3 install flask-swagger

# Configure DCS Dashboards service
RUN mvn clean install -DskipTests -f /tmp/5geve-wp4-dcs-kibana-dashboards-handler/kibana-dashboards
RUN sed -i -e 's/password.*/password: changeme/' /tmp/5geve-wp4-dcs-kibana-dashboards-handler/src/main/resources/application.yml
RUN sed -i -e 's/oauth-enabled.*/oauth-enabled: false/' /tmp/5geve-wp4-dcs-kibana-dashboards-handler/src/main/resources/application.yml
RUN sed -i -e 's/dashboard-owner-enabled.*/dashboard-owner-enabled: false/' /tmp/5geve-wp4-dcs-kibana-dashboards-handler/src/main/resources/application.yml

# Environment variable for network commands, if needed
ENV network_commands=false

# Copy run_logstash.sh script
#COPY files/run_logstash.sh /usr/bin/dcs
#RUN chmod +x /usr/bin/dcs/run_logstash.sh

# Entrypoint script
COPY files/entrypoint.sh /
RUN chmod +x entrypoint.sh
ENTRYPOINT /bin/bash entrypoint.sh
