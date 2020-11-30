#!/bin/bash
dcs_rest_client_ip_port=$1
create_kafka_topic_ip_port=$2
delete_kafka_topic_ip_port=$3
fetch_kafka_topic_ip_port=$4

# Start DCM
echo "Start DCM"
/usr/bin/python3 dcm.py --dcs_rest_client_ip_port $dcs_rest_client_ip_port --create_kafka_topic_ip_port $create_kafka_topic_ip_port --delete_kafka_topic_ip_port $delete_kafka_topic_ip_port --fetch_kafka_topic_ip_port $fetch_kafka_topic_ip_port --log info > /var/log/dcm.log
