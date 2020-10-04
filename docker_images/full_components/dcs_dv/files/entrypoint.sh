#!/bin/bash

# Modify Kibana configuration that depends on environment variables
sed -i -e "s/DCS_IP_ADDRESS=/DCS_IP_ADDRESS=$kibana_ip_address/" /usr/bin/dcs/refresh_dashboard.sh
#sed -i -e "s/#server.host: \"localhost\"/server.host: \"$kibana_ip_address\"/" /etc/kibana/kibana.yml
sed -i -e "s/#server.host: \"localhost\"/server.host: \"0.0.0.0\"/" /etc/kibana/kibana.yml
sed -i -e "s;#elasticsearch.hosts: \[\"http://localhost:9200\"\];elasticsearch.hosts: [$elasticsearch_hosts];" /etc/kibana/kibana.yml

# Modify Logstash configuration that depends on environment variables
sed -i -e "s/DCS_IP_ADDRESS=/DCS_IP_ADDRESS=$elasticsearch_ip_address/" /usr/bin/dcs/create_logstash_pipeline.sh
sed -i -e "s/DCM_IP_ADDRESS=/DCM_IP_ADDRESS=$dcm_ip_address/" /usr/bin/dcs/create_logstash_pipeline.sh
sed -i -e "s/DCS_IP_ADDRESS=/DCS_IP_ADDRESS=$elasticsearch_ip_address/" /usr/bin/dcs/delete_logstash_pipeline.sh
sed -i -e "s;#xpack.monitoring.elasticsearch.hosts: \[\"https://es1:9200\", \"https://es2:9200\"\];xpack.monitoring.elasticsearch.hosts: [$elasticsearch_hosts];" /etc/logstash/logstash.yml

# Configure and start PostgreSQL
/etc/init.d/postgresql start
#sudo -u postgres createuser eve
#sudo -u postgres createdb dashboards
#sudo -u postgres createdb pipelines
sudo -u postgres psql -f /tmp/script_db.sql
sudo -u postgres psql -f /tmp/script_table.sql -d pipelines
rm /tmp/*.sql

# Modify DCS Dashboards service configuration that depends on environment variables and build the project
sed -i -e "s;baseUrl.*;baseUrl: http://$kibana_ip_address:5601;" /tmp/5geve-wp4-dcs-kibana-dashboards-handler/src/main/resources/application.yml
mvn clean install -DskipTests -f /tmp/5geve-wp4-dcs-kibana-dashboards-handler
mv /tmp/5geve-wp4-dcs-kibana-dashboards-handler/target/dcs-0.0.1-SNAPSHOT.jar /usr/bin/dcs/dcs_dashboard.jar && chmod 664 /usr/bin/dcs/dcs_dashboard.jar
rm -r /tmp/5geve-wp4-dcs-kibana-dashboards-handler

# Execute commands from network_commands
bash -c "$network_commands"

# Start ELK Stack (without Logstash)
/etc/init.d/elasticsearch start
#source /etc/default/logstash
#/usr/share/logstash/bin/logstash "--path.settings" "/etc/logstash" > /var/log/logstash.log &
/etc/init.d/kibana start

# Start DCS Dashboards service
echo "Start DCS Dashboard"
/usr/bin/java -jar /usr/bin/dcs/dcs_dashboard.jar > /var/log/dcs_dashboard.log &

# Start DCS
echo "Start DCS"
/usr/bin/python3 /usr/bin/dcs/dcs-python/dcs_rest_client.py --dcm_ip_address $dcm_ip_address --eve_db_password changeme --port 8091 --log info > /var/log/dcs.log
