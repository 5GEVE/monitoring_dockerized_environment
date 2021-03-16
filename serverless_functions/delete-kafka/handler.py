#!/usr/bin/env python3

import json

from kafka.admin import KafkaAdminClient


def handle(event, context):
    if event.method == "POST":
        try:
            data = json.loads(event.body)
            topic = data["topic"]

            admin_client = KafkaAdminClient(
                bootstrap_servers="kafka.deployment8:9092",
                client_id="delete_kafka_topic",
            )

            admin_client.delete_topics(topics=[topic])
            admin_client.close()
            return {"statusCode": 201, "body": "No Content"}
        except Exception as e:
            return {"statusCode": 400, "body": f"Error parsing request: {e}"}
    else:
        return {"statusCode": 200, "body": "No action for this endpoint"}
