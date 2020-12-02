#!/bin/bash

# Start Zookeeper
echo "Start Zookeeper"
sleep 5
/bin/bash /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
