import requests
import argparse
import logging
import coloredlogs
from flask import Flask, request, jsonify
from flask_swagger import swagger
from waitress import serve
import json


app = Flask(__name__)
logger = logging.getLogger("DCMRestClient")


@app.route('/', methods=['GET'])
def server_status():
    logger.info("GET /")
    return '', 200


@app.route("/spec", methods=['GET'])
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "DCM REST API"
    return jsonify(swag)


def check_if_topic_exist(topic):
    logger.info("Checking if topic %s exists in Kafka", topic)
    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.get(url_fetch_kafka_topic, json=request_body)
    logger.info("Response: Code %s", r)

    topic_exist = False

    if r.status_code == 302:
        topic_exist = True
    elif r.status_code == 404:
        topic_exist = False
    else:
        logger.warning("Wrong operation")

    return topic_exist


def send_data_to_dcs(data, operation):
    logger.info("Send data to DCS. Data: %s, Operation: %s", data, operation)
    request_body = json.loads(json.dumps(data))

    if operation == "subscribe":
        r = requests.post(url_dcs_subscribe, json=request_body)
        logger.info("Response: Code %s", r)
    elif operation == "unsubscribe":
        r = requests.delete(url_dcs_unsubscribe, json=request_body)
        logger.info("Response: Code %s", r)
    else:
        logger.warning("Wrong operation: %s", operation)


def create_kafka_topic(topic):
    logger.info("Creating topic %s in Kafka", topic)
    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.post(url_create_kafka_topic, json=request_body)
    logger.info("Response: Code %s", r)


@app.route('/dcm/subscribe', methods=['POST'])
def subscribe():
    logger.info("Request received - POST /dcm/subscribe")
    if not request.is_json:
        logger.warning("Format not valid")
        return 'Format not valid', 400
    try:
        data = request.get_json()
        records = data["records"]
        logger.info("Records raw list: %s", records)
        for value in records:
            if value["value"]["topic"].count('.') != 4 or value["value"]["topic"].count(' ') != 0 or value["value"]["topic"].count(',') != 0:
                raise Exception("Incorrect format in topic name: %s", value["value"]["topic"])
            else:
                logger.info("Value received: topic %s - expId %s - action %s - context %s", value["value"]["topic"], value["value"]["expId"], value["value"]["action"], value["value"]["context"])
                    
                kafka_topic = value["value"]["topic"]

                if check_if_topic_exist(kafka_topic) == False:
                    create_kafka_topic(kafka_topic)
                    send_data_to_dcs(value, "subscribe")
                else:
                    logger.warning("The topic %s already exists in Kafka", kafka_topic)
    except Exception as e:
        logger.error("Error while parsing request")
        logger.exception(e)
        return str(e), 400
    return '', 201


def delete_kafka_topic(topic):
    logger.info("Deleting topic %s in Kafka", topic)
    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.delete(url_delete_kafka_topic, json=request_body)
    logger.info("Response: Code %s", r)


@app.route('/dcm/unsubscribe', methods=['DELETE'])
def unsubscribe():
    logger.info("Request received - DELETE /dcm/unsubscribe")
    if not request.is_json:
        logger.warning("Format not valid")
        return 'Format not valid', 400
    try:
        data = request.get_json()
        records = data["records"]
        logger.info("Records raw list: %s", records)
        for value in records:
            if value["value"]["topic"].count('.') != 4 or value["value"]["topic"].count(' ') != 0 or value["value"]["topic"].count(',') != 0:
                raise Exception("Incorrect format in topic name: %s", value["value"]["topic"])
            else:
                logger.info("Value received: topic %s - expId %s - action %s - context %s", value["value"]["topic"], value["value"]["expId"], value["value"]["action"], value["value"]["context"])
                    
                kafka_topic = value["value"]["topic"]

                if check_if_topic_exist(kafka_topic) == True:
                    send_data_to_dcs(value, "unsubscribe")
                    delete_kafka_topic(kafka_topic)
                else:
                    logger.warning("The topic %s does not exist in Kafka", kafka_topic)
    except Exception as e:
        logger.error("Error while parsing request")
        logger.exception(e)
        return str(e), 400
    return '', 201


if __name__ == "__main__":
    # Usage: /usr/bin/python3 dcm_rest_client.py --dcs_rest_client_ip_port localhost:8091 --create_kafka_topic_ip_port localhost:8190 --delete_kafka_topic_ip_port localhost:8290 --fetch_kafka_topic_ip_port localhost:8390 --log info
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dcs_rest_client_ip_port",
        help='DCS REST Client IP:port',
        default='localhost:8091')
    parser.add_argument(
        "--create_kafka_topic_ip_port",
        help='createKafkaTopic function IP:port',
        default='localhost:8190')
    parser.add_argument(
        "--delete_kafka_topic_ip_port",
        help='deleteKafkaTopic function IP:port',
        default='localhost:8290')
    parser.add_argument(
        "--fetch_kafka_topic_ip_port",
        help='listKafkaTopics function IP:port',
        default='localhost:8390')
    parser.add_argument(
        "--log",
        help='Sets the Log Level output, default level is "info"',
        choices=[
            "info",
            "debug",
            "error",
            "warning"],
        nargs='?',
        default='info')

    args = parser.parse_args()
    numeric_level = getattr(logging, str(args.log).upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    coloredlogs.install(
        fmt='%(asctime)s %(levelname)s %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=numeric_level)
    logging.getLogger("DCMRestClient").setLevel(numeric_level)
    logging.getLogger("requests.packages.urllib3").setLevel(logging.ERROR)

    global dcs_rest_client_ip_port 
    dcs_rest_client_ip_port = str(args.dcs_rest_client_ip_port)
    global url_dcs_subscribe
    url_dcs_subscribe = "http://" + dcs_rest_client_ip_port + "/portal/dcs/subscribe"
    global url_dcs_unsubscribe
    url_dcs_unsubscribe = "http://" + dcs_rest_client_ip_port + "/portal/dcs/unsubscribe"

    global create_kafka_topic_ip_port 
    create_kafka_topic_ip_port = str(args.create_kafka_topic_ip_port)
    global url_create_kafka_topic
    url_create_kafka_topic = "http://" + create_kafka_topic_ip_port + "/create_kafka_topic"
    
    global delete_kafka_topic_ip_port
    delete_kafka_topic_ip_port = str(args.delete_kafka_topic_ip_port)
    global url_delete_kafka_topic
    url_delete_kafka_topic = "http://" + delete_kafka_topic_ip_port + "/delete_kafka_topic"
    
    global fetch_kafka_topic_ip_port 
    fetch_kafka_topic_ip_port = str(args.fetch_kafka_topic_ip_port)    
    global url_fetch_kafka_topic
    url_fetch_kafka_topic = "http://" + fetch_kafka_topic_ip_port + "/fetch_kafka_topic"

    logger.info("Serving DCMRestClient on port 8090")

    serve(app, host='0.0.0.0', port=8090)
