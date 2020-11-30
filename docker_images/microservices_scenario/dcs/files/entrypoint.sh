#!/bin/bash
dcs_dashboard_ip_port=$1
logstash_pipeline_manager_ip_port=$2
kafka_consumer_ip_port=$3
elasticsearch_ip_port=$4

# Start DCS
echo "Start DCS"
/usr/bin/python3 dcs.py --dcs_dashboard_ip_port $dcs_dashboard_ip_port --logstash_pipeline_manager_ip_port $logstash_pipeline_manager_ip_port --kafka_consumer_ip_port $kafka_consumer_ip_port --elasticsearch_ip_port $elasticsearch_ip_port --elk_password changeme --log info > /var/log/dcs.log
