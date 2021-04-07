#!/bin/bash
elasticsearch_hosts=$1
kafka_ip_port=$2
elasticsearch_ip_port=$3

# Modify Logstash configuration that depends on environment variables
sed -i -e "s;#xpack.monitoring.elasticsearch.hosts: \[\"https://es1:9200\", \"https://es2:9200\"\];xpack.monitoring.elasticsearch.hosts: [$elasticsearch_hosts];" /etc/logstash/logstash.yml

# Start Logstash Pipeline Manager
echo "Start Logstash Pipeline Manager"
/usr/bin/python3 /usr/bin/dcs/logstash_pipeline_manager.py --script_path /usr/bin/dcs --kafka_ip_port $kafka_ip_port --elasticsearch_ip_port $elasticsearch_ip_port --elk_password changeme --log info > /var/log/logstash_pipeline_manager.log
