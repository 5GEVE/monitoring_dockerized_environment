FROM ubuntu:xenial

# Install packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jre openjdk-8-jdk curl nano git iputils-ping apt-transport-https wget nginx jq maven

# Set JAVA_HOME
RUN sed -i '/^JAVA_HOME.*/d' /etc/environment && echo JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd4 | tee -a /etc/environment > /dev/null

# Install ELK Stack
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
ADD https://artifacts.elastic.co/downloads/kibana/kibana-7.5.0-amd64.deb /tmp
RUN dpkg -i /tmp/kibana-7.5.0-amd64.deb
RUN rm /tmp/*.deb

# Create /usr/bin/dcs directory
RUN mkdir -p /usr/bin/dcs/
RUN chmod 755 /usr/bin/dcs/
RUN chown root:root /usr/bin/dcs/

# Download 5geve-wp4-dcs-kibana-dashboards-handler and 5geve-wp4-dcs-kibana-dashboards-generator
RUN mkdir -p /tmp/5geve-wp4-dcs-kibana-dashboards-handler
RUN git clone -b v0.1 https://github.com/5GEVE/5geve-wp4-dcs-kibana-dashboards-handler.git /tmp/5geve-wp4-dcs-kibana-dashboards-handler
RUN mkdir -p /tmp/5geve-wp4-dcs-kibana-dashboards-handler/5geve-wp4-dcs-kibana-dashboards-generator
RUN git clone --recursive -b v0.1 https://github.com/5GEVE/5geve-wp4-dcs-kibana-dashboards-generator.git /tmp/5geve-wp4-dcs-kibana-dashboards-handler/5geve-wp4-dcs-kibana-dashboards-generator
RUN rm -rf /tmp/5geve-wp4-dcs-kibana-dashboards-handler/kibana-dashboards && mv /tmp/5geve-wp4-dcs-kibana-dashboards-handler/5geve-wp4-dcs-kibana-dashboards-generator /tmp/5geve-wp4-dcs-kibana-dashboards-handler/kibana-dashboards

# Configure Kibana
#RUN sed -i -e "s/PASSWORD=/PASSWORD=changeme/" /usr/bin/dcs/refresh_dashboard.sh
RUN sed -i -e 's/#server.name: "your-hostname"/server.name: kibana/' /etc/kibana/kibana.yml
RUN sed -i -e 's/#elasticsearch.username: "kibana"/elasticsearch.username: elastic/' /etc/kibana/kibana.yml
RUN sed -i -e 's/#elasticsearch.password: "pass"/elasticsearch.password: changeme/' /etc/kibana/kibana.yml
RUN echo "xpack.security.enabled: false" | tee -a /etc/kibana/kibana.yml > /dev/null

# Install and configure PostgreSQL
COPY files/script_db.sql /tmp
RUN apt-get install -y postgresql postgresql-contrib python3-psycopg2 sudo
#RUN /etc/init.d/postgresql start
#RUN sudo -u postgres createuser eve
#RUN sudo -u postgres createdb dashboards
#RUN sudo -u postgres createdb pipelines
#RUN sudo -u postgres psql -f /tmp/script_db.sql
# Test to access DB: sudo -u postgres psql eve -h 127.0.0.1 -d dashboards

# Configure DCS Dashboards service
RUN mvn clean install -DskipTests -f /tmp/5geve-wp4-dcs-kibana-dashboards-handler/kibana-dashboards
RUN sed -i -e 's/password.*/password: changeme/' /tmp/5geve-wp4-dcs-kibana-dashboards-handler/src/main/resources/application.yml
RUN sed -i -e 's/oauth-enabled.*/oauth-enabled: false/' /tmp/5geve-wp4-dcs-kibana-dashboards-handler/src/main/resources/application.yml
RUN sed -i -e 's/dashboard-owner-enabled.*/dashboard-owner-enabled: false/' /tmp/5geve-wp4-dcs-kibana-dashboards-handler/src/main/resources/application.yml

# Entrypoint script
COPY files/entrypoint.sh /
RUN chmod +x entrypoint.sh
#CMD /entrypoint.sh kibana "http://elasticsearch:9200"
CMD ["/entrypoint.sh", "kibana", "\"http://elasticsearch:9200\""]
