#!/bin/bash
kafka_ip_port=$1

# Start Create Kafka Topic
echo "Start Create Kafka Topic"
/usr/bin/python3 create_kafka_topic.py --kafka_ip_port $kafka_ip_port --log info > /var/log/create_kafka_topic.log
