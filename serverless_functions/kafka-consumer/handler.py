#!/usr/bin/env python3

import json
import time

from kafka import KafkaConsumer
from requests import post


def handle(event, context):
    if event.method == "POST":
        try:
            data = json.loads(event.body)
            topic = data["topic"]
            value = data["value"]
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=["kafka.deployment8:9092"],
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id=None,
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )

            message_received = False
            while not message_received:
                message = consumer.poll(timeout_ms=1000)
                if message != {}:
                    message_received = True
            consumer.close()

            time.sleep(5)  # needed?
            post(
                "http://kibana.deployment8:8080/portal/dcs/dashboard",
                json=json.loads(json.dumps({"records": [{"value": value}]})),
            )
            return {"statusCode": 201, "body": "No Content"}
        except Exception as e:
            return {"statusCode": 400, "body": f"Error parsing request: {e}"}
    else:
        return {"statusCode": 200, "body": "No action for this endpoint"}
