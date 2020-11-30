#!/bin/bash
kafka_ip_port=$1

# Start Delete Kafka Topic
echo "Start Delete Kafka Topic"
/usr/bin/python3 delete_kafka_topic.py --kafka_ip_port $kafka_ip_port --log info > /var/log/delete_kafka_topic.log
