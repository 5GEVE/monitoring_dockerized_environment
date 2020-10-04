#!/bin/bash

TOPIC=$1
TOPIC_LOWERCASE=$(echo "$TOPIC" | awk '{print tolower($0)}')
DCS_IP_ADDRESS=
DCM_IP_ADDRESS=
USER=elastic
PASSWORD=

curl --location --request PUT "${DCS_IP_ADDRESS}:9200/${TOPIC_LOWERCASE}" -u ${USER}:${PASSWORD}

if [[ $TOPIC == *"metric."* ]]; then
	echo "input { kafka { bootstrap_servers => '${DCM_IP_ADDRESS}:9092' client_id => 'logstash' client_rack => 'dcm' topics => '$TOPIC' } } filter { ruby { code => \"event.set('message_size', event.get('message').bytesize)\" } json { source => \"message\" } if \"_jsonparsefailure\" in [tags] { drop { } } else { split { field => \"records\" } if \"_split_type_failure\" in [tags] { drop { } } else { mutate { rename => { \"[records][value][metric_value]\" => \"metric_value\" \"[records][value][timestamp]\" => \"timestamp\" \"[records][value][unit]\" => \"unit\" \"[records][value][device_id]\" => \"device_id\" \"[records][value][context]\" => \"context\" } remove_field => [\"message\"] convert => { \"metric_value\" => \"float\" } } date { match => [\"timestamp\", \"UNIX\"] target => \"device_timestamp\" remove_field => \"timestamp\" } } } } output { elasticsearch { hosts => \"${DCS_IP_ADDRESS}:9200\" index => \"$TOPIC_LOWERCASE\" user => \"$USER\" password => \"$PASSWORD\" } }" | sudo tee -a /etc/logstash/conf.d/${TOPIC}.conf > /dev/null;
elif [[ $TOPIC == *"kpi."* ]]; then
	echo "input { kafka { bootstrap_servers => '${DCM_IP_ADDRESS}:9092' client_id => 'logstash' client_rack => 'dcm' topics => '$TOPIC' } } filter { ruby { code => \"event.set('message_size', event.get('message').bytesize)\" } json { source => \"message\" } if \"_jsonparsefailure\" in [tags] { drop { } } else { split { field => \"records\" } if \"_split_type_failure\" in [tags] { drop { } } else { mutate { rename => { \"[records][value][kpi_value]\" => \"kpi_value\" \"[records][value][timestamp]\" => \"timestamp\" \"[records][value][unit]\" => \"unit\" \"[records][value][device_id]\" => \"device_id\" \"[records][value][context]\" => \"context\" } remove_field => [\"message\"] convert => { \"kpi_value\" => \"float\" } } date { match => [\"timestamp\", \"UNIX\"] target => \"device_timestamp\" remove_field => \"timestamp\" } } } } output { elasticsearch { hosts => \"${DCS_IP_ADDRESS}:9200\" index => \"$TOPIC_LOWERCASE\" user => \"$USER\" password => \"$PASSWORD\" } }" | sudo tee -a /etc/logstash/conf.d/${TOPIC}.conf > /dev/null;
fi

# to show output: ... output { stdout { codec => rubydebug } elasticsearch ...

echo $'- pipeline.id: '${TOPIC}$'\n  path.config: "/etc/logstash/conf.d/'${TOPIC}'.conf"' | sudo tee -a /etc/logstash/pipelines.yml > /dev/null
