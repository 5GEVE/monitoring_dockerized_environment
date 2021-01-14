#!/bin/bash

TOPIC=$1

sed -i $(cat /etc/logstash/pipelines.yml | grep -n ${TOPIC} | awk '{print $1 "d"}' | sed 's/[^0-9a-zA-Z]//g' | sed ':a;N;$!ba;s/\n/;/g') /etc/logstash/pipelines.yml
rm /etc/logstash/conf.d/${TOPIC}.conf
