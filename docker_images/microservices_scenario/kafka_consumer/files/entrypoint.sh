#!/bin/bash
dcs_dashboard_ip_port=$1
kafka_ip_port=$2

# Start Kafka Consumer
echo "Start Kafka Consumer"
/usr/bin/python3 kafka_consumer.py --dcs_dashboard_ip_port $dcs_dashboard_ip_port --kafka_ip_port $kafka_ip_port --log info > /var/log/kafka_consumer.log
