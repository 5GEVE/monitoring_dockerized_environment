#!/usr/bin/env python3

import requests
import json
import threading
from threading import Thread
from threading import Timer
from datetime import timedelta
import time

def create_elasticsearch_index(topic):
    url_elasticsearch = "http://elasticsearch.deployment8:9200"
    r = requests.put(url_elasticsearch + "/" + topic, auth=('elastic', 'changeme'))

def create_logstash_pipeline(topic):
    url_logstash_pipeline_manager = "http://logstash.deployment8:8191/logstash_pipeline_manager"

    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.post(url_logstash_pipeline_manager, json=request_body)

def kafka_consumer(value):
    url_kafka_consumer = "http://10.244.0.97:8080/function/kafka-consumer"

    request_body = json.loads(json.dumps({'value': value}))
    r = requests.post(url_kafka_consumer, json=request_body)

def delete_logstash_pipeline(topic):
    url_logstash_pipeline_manager = "http://logstash.deployment8:8191/logstash_pipeline_manager"

    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.delete(url_logstash_pipeline_manager, json=request_body)

def index_cleaner(topic, value):

    url_dcs_dashboard = "http://kibana.deployment8:8080/portal/dcs/dashboard"
    url_elasticsearch = "http://elasticsearch.deployment8:9200"

    r_first = requests.delete(url_dcs_dashboard, json=json.loads(json.dumps({'records': [ { 'value': value }]})))
    r_second = requests.delete(url_elasticsearch + "/" + topic, auth=('elastic', 'changeme'))

def handle(event, context):
    if event.method == "POST":
        try:
            data = json.loads(event.body)
            value = data["value"]
            topic = value["topic"]
            create_elasticsearch_index(topic.lower())
            create_logstash_pipeline(topic)
            kafka_consumer(value)

            return {"statusCode": 201, "body": "No Content"}
        except Exception as e:
            return {"statusCode": 400, "body": "Error parsing request: {e}"}

    elif event.method == "DELETE":
        try:
            data = json.loads(event.body)
            value = data["value"]
            topic = value["topic"]
            delete_logstash_pipeline(topic)
            index_cleaner(topic.lower(), value)

            return {"statusCode": 201, "body": "No Content"}
        except Exception as e:
            return {"statusCode": 400, "body": "Error parsing request: {e}"}

    else:
        return {"statusCode": 200, "body": "No action for this endpoint"}
