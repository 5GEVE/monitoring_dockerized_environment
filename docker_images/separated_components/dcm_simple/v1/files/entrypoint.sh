#!/bin/bash

# Modify /opt/kafka/config/server.properties (lines with environment variables)
echo "Modify /opt/kafka/config/server.properties"
sed -i -e "s;#listeners=PLAINTEXT://:9092;listeners=$listener_ip_addresses;" /opt/kafka/config/server.properties
sed -i -e "s;#advertised.listeners=PLAINTEXT://your.host.name:9092;advertised.listeners=$adv_listener_ip_addresses;" /opt/kafka/config/server.properties
sed -i -e "s/broker.id=0/broker.id=$broker_id/" /opt/kafka/config/server.properties
sed -i -e "s/zookeeper.connect=localhost:2181/zookeeper.connect=$zookeeper_ip_address:2181/" /opt/kafka/config/server.properties
echo "listener.security.protocol.map=$listener_security_protocol_map" | tee -a /opt/kafka/config/server.properties > /dev/null
echo "inter.broker.listener.name=$inter_broker_listener_name" | tee -a /opt/kafka/config/server.properties > /dev/null
echo "broker.rack=$rack_name" | tee -a /opt/kafka/config/server.properties > /dev/null

# Execute commands from network_commands
bash -c "$network_commands"

# Start Kafka in background
echo "Start Kafka in background"
sleep 5
/bin/bash /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties &
sleep 20

# Start DCM
echo "Start DCM"
/usr/bin/python3 /usr/bin/dcm/dcm-python/dcm_rest_client.py --dcm_ip_address $dcm_ip_address --zookeeper_ip_address $zookeeper_ip_address --kafka_port $kafka_port --port 8090 --log info
