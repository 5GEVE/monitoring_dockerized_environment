#!/bin/bash
listener_ip_addresses=$1
adv_listener_ip_addresses=$2
#broker_id=$3
zookeeper_ip_address=$3
#rack_name=$5

# Modify /opt/kafka/config/server.properties (lines with environment variables)
echo "Modify /opt/kafka/config/server.properties"
sed -i -e "s;#listeners=PLAINTEXT://:9092;listeners=$listener_ip_addresses;" /opt/kafka/config/server.properties
sed -i -e "s;#advertised.listeners=PLAINTEXT://your.host.name:9092;advertised.listeners=$adv_listener_ip_addresses;" /opt/kafka/config/server.properties
#sed -i -e "s/broker.id=0/broker.id=$broker_id/" /opt/kafka/config/server.properties
sed -i -e "s/zookeeper.connect=localhost:2181/zookeeper.connect=$zookeeper_ip_address:2181/" /opt/kafka/config/server.properties
#echo "broker.rack=$rack_name" | tee -a /opt/kafka/config/server.properties > /dev/null

# Start Kafka
echo "Start Kafka"
sleep 5
/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties
