#!/usr/bin/env python3

import requests
import json

def check_if_topic_exist(topic):

    url_fetch_kafka_topic = "http://10.244.0.97:8080/function/fetch-kafka"

    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.get(url_fetch_kafka_topic, json=request_body)

    topic_exist = False

    if r.status_code == 302:
        topic_exist = True
    elif r.status_code == 404:
        topic_exist = False

    return topic_exist


def send_data_to_dcs(data, operation):

    request_body = json.loads(json.dumps(data))

    if operation == "subscribe":
        url_dcs_subscribe = "http://10.244.0.97:8080/function/dcs"
        r = requests.post(url_dcs_subscribe, json=request_body)
    elif operation == "unsubscribe":
        url_dcs_unsubscribe = "http://10.244.0.97:8080/function/dcs"
        r = requests.delete(url_dcs_unsubscribe, json=request_body)

def create_kafka_topic(topic):

    url_create_kafka_topic = "http://10.244.0.97:8080/function/create-kafka"

    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.post(url_create_kafka_topic, json=request_body)

def delete_kafka_topic(topic):

    url_delete_kafka_topic = "http://10.244.0.97:8080/function/delete-kafka"

    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.post(url_delete_kafka_topic, json=request_body)

def handle(event, context):
    if event.method == "POST":
        try:
            data = json.loads(event.body)
            records = data["records"]
            for value in records:
                if value["value"]["topic"].count('.') != 4 or value["value"]["topic"].count(' ') != 0 or value["value"]["topic"].count(',') != 0:
                    raise Exception("Incorrect format in topic name: %s", value["value"]["topic"])
                else:                        
                    kafka_topic = value["value"]["topic"]

                    if check_if_topic_exist(kafka_topic) == False:
                        create_kafka_topic(kafka_topic)
                        send_data_to_dcs(value, "subscribe")
                        return {"statusCode": 201, "body": "No Content"}
                    else:
                        return {"statusCode": 500, "body": "Topic already exists in Kafka"}

        except Exception as e:
            return {"statusCode": 400, "body": "Error parsing request: {e}"}

    elif event.method == "DELETE":
        try:
            data = json.loads(event.body)
            records = data["records"]
            for value in records:
                if value["value"]["topic"].count('.') != 4 or value["value"]["topic"].count(' ') != 0 or value["value"]["topic"].count(',') != 0:
                    raise Exception("Incorrect format in topic name: %s", value["value"]["topic"])
                else:                        
                    kafka_topic = value["value"]["topic"]

                    if check_if_topic_exist(kafka_topic) == True:
                        send_data_to_dcs(value, "unsubscribe")
                        delete_kafka_topic(kafka_topic)
                        return {"statusCode": 201, "body": "No Content"}
                    else:
                        return {"statusCode": 500, "body": "Topic does not exist in Kafka"}

        except Exception as e:
            return {"statusCode": 400, "body": "Error parsing request: {e}"}

    else:
        return {"statusCode": 200, "body": "No action for this endpoint"}
