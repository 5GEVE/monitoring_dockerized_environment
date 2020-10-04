#!/bin/bash

TOPIC=$1
TOPIC_LOWERCASE=$(echo "$TOPIC" | awk '{print tolower($0)}')
DCS_IP_ADDRESS=
USER=elastic
PASSWORD=
DELETE_INDEX=$2

if [ "$DELETE_INDEX" == "yes" ]; then
    curl --location --request DELETE "${DCS_IP_ADDRESS}:9200/${TOPIC_LOWERCASE}" -u ${USER}:${PASSWORD}
else
    sudo sed -i $(cat /etc/logstash/pipelines.yml | grep -n ${TOPIC} | awk '{print $1 "d"}' | sed 's/[^0-9a-zA-Z]//g' | sed ':a;N;$!ba;s/\n/;/g') /etc/logstash/pipelines.yml
    sudo rm /etc/logstash/conf.d/${TOPIC}.conf
fi
