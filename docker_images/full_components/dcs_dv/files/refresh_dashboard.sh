#!/bin/bash

TOPIC=$1
TOPIC_LOWERCASE=$(echo "$TOPIC" | awk '{print tolower($0)}')
DCS_IP_ADDRESS=
USER=elastic
PASSWORD=

fields_available="0"

while [ "$fields_available" == "0" ]
do
    refresh_payload=$(curl -X GET -u ${USER}:${PASSWORD} "http://${DCS_IP_ADDRESS}:5601/api/index_patterns/_fields_for_wildcard?pattern=${TOPIC_LOWERCASE}&meta_fields=\[%22_source%22,%22_index%22,%22_id%22,%20%22_score%22,%20%22_type%22\]" | jq '.fields[] | . + {count: 0} | . + {scripted: false}' | jq -s  --arg TITLE "${TOPIC_LOWERCASE}" '. | tostring | {"attributes": {"title": $TITLE, "timeFieldName": "@timestamp", "fields": . }}')
    fields_available=$(echo $refresh_payload | grep device_timestamp | wc -l)
    if [ "$fields_available" != "0" ]; then
        curl -X PUT -u ${USER}:${PASSWORD} "http://${DCS_IP_ADDRESS}:5601/api/saved_objects/index-pattern/${TOPIC_LOWERCASE}" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d "$refresh_payload"
    fi
done
