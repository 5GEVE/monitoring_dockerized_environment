#!/bin/bash
kibana_ip_address=$1
elasticsearch_hosts=$2

# Modify Kibana configuration that depends on environment variables
#sed -i -e "s/#server.host: \"localhost\"/server.host: \"$kibana_ip_address\"/" /etc/kibana/kibana.yml
sed -i -e "s/#server.host: \"localhost\"/server.host: \"0.0.0.0\"/" /etc/kibana/kibana.yml
sed -i -e "s;#elasticsearch.hosts: \[\"http://localhost:9200\"\];elasticsearch.hosts: [$elasticsearch_hosts];" /etc/kibana/kibana.yml

# Configure and start PostgreSQL
/etc/init.d/postgresql start
#sudo -u postgres createuser eve
#sudo -u postgres createdb dashboards
#sudo -u postgres createdb pipelines
sudo -u postgres psql -f /tmp/script_db.sql
rm /tmp/*.sql

# Modify DCS Dashboards service configuration that depends on environment variables and build the project
sed -i -e "s;baseUrl.*;baseUrl: http://$kibana_ip_address:5601;" /tmp/5geve-wp4-dcs-kibana-dashboards-handler/src/main/resources/application.yml
mvn clean install -DskipTests -f /tmp/5geve-wp4-dcs-kibana-dashboards-handler
mv /tmp/5geve-wp4-dcs-kibana-dashboards-handler/target/dcs-0.0.1-SNAPSHOT.jar /usr/bin/dcs/dcs_dashboard.jar && chmod 664 /usr/bin/dcs/dcs_dashboard.jar
rm -r /tmp/5geve-wp4-dcs-kibana-dashboards-handler

# Start Kibana
/etc/init.d/kibana start

# Start DCS Dashboards service
echo "Start DCS Dashboard"
/usr/bin/java -jar /usr/bin/dcs/dcs_dashboard.jar > /var/log/dcs_dashboard.log &
tail -f /var/log/dcs_dashboard.log
