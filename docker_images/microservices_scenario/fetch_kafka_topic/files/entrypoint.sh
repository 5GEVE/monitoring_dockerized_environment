#!/bin/bash
kafka_ip_port=$1

# Start Fetch Kafka Topic
echo "Start Fetch Kafka Topic"
/usr/bin/python3 fetch_kafka_topic.py --kafka_ip_port $kafka_ip_port --log info > /var/log/fetch_kafka_topic.log
