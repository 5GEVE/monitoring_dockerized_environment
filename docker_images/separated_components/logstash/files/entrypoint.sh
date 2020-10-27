#!/bin/bash
elasticsearch_ip_address=$1
dcm_ip_address=$2
elasticsearch_hosts=$3
kibana_ip_address=$4

# Modify Logstash configuration that depends on environment variables
sed -i -e "s/DCS_IP_ADDRESS=/DCS_IP_ADDRESS=$elasticsearch_ip_address/" /usr/bin/dcs/create_logstash_pipeline.sh
sed -i -e "s/DCM_IP_ADDRESS=/DCM_IP_ADDRESS=$dcm_ip_address/" /usr/bin/dcs/create_logstash_pipeline.sh
sed -i -e "s/DCS_IP_ADDRESS=/DCS_IP_ADDRESS=$elasticsearch_ip_address/" /usr/bin/dcs/delete_logstash_pipeline.sh
sed -i -e "s;#xpack.monitoring.elasticsearch.hosts: \[\"https://es1:9200\", \"https://es2:9200\"\];xpack.monitoring.elasticsearch.hosts: [$elasticsearch_hosts];" /etc/logstash/logstash.yml
# Extra: Kibana IP address must be changed in Python handler
sed -i -e "s/127.0.0.1/$kibana_ip_address/" /usr/bin/dcs/dcs-python/dcs_rest_client.py

# Configure and start PostgreSQL
/etc/init.d/postgresql start
#sudo -u postgres createuser eve
#sudo -u postgres createdb dashboards
#sudo -u postgres createdb pipelines
sudo -u postgres psql -f /tmp/script_db.sql
sudo -u postgres psql -f /tmp/script_table.sql -d pipelines
rm /tmp/*.sql

# Start DCS
echo "Start DCS"
/usr/bin/python3 /usr/bin/dcs/dcs-python/dcs_rest_client.py --dcm_ip_address $dcm_ip_address --eve_db_password changeme --port 8091 --log info > /var/log/dcs.log
