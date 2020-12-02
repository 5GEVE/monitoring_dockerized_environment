import requests
import argparse
import logging
import coloredlogs
import threading
from flask import Flask, request, jsonify
from flask_swagger import swagger
from waitress import serve
import subprocess
import json
from kafka import KafkaConsumer
from threading import Thread
import time


app = Flask(__name__)
logger = logging.getLogger("KafkaConsumer")


@app.route('/', methods=['GET'])
def server_status():
    logger.info("GET /")
    return '', 200


@app.route("/spec", methods=['GET'])
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "KafkaConsumer REST API"
    return jsonify(swag)


def kafka_consumer_refresh_dashboard_handler(topic, value):
    logger.info("Creating Kafka Consumer for %s topic", topic)
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[kafka_ip_port],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=None,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    message_received = False
    while not message_received:
        message = consumer.poll(timeout_ms=1000)
        if message != {}:
            logger.info("Message received in %s topic: %s", topic, message)
            message_received = True

    time.sleep(5)
    logger.info("Creating dashboard for topic: %s", topic)            
    r = requests.post(url_dcs_dashboard, json=json.loads(json.dumps({'records': [ { 'value': value }]})))
    logger.info("Response: Code %s", r)

    # This call seems that is not needed as the dashboard is generated when data is present.
    #time.sleep(2)            
    #logger.info("Refreshing dashboard for %s topic", topic)
    #subprocess.call(['/bin/bash', '/usr/bin/dcs/refresh_dashboard.sh', topic])

    logger.info("Closing Kafka Consumer for %s topic", topic)
    consumer.close()


@app.route('/kafka_consumer', methods=['POST'])
def kafka_consumer():
    logger.info("Request received - POST /kafka_consumer")
    if not request.is_json:
        logger.warning("Format not valid")
        return 'Format not valid', 400
    try:
        data = request.get_json()
        value = data["value"]
        topic = value["topic"]

        # Create Kafka consumer to wait for the first message received in the topic and, then, refresh the dashboard.
        thread = threading.Thread(target = kafka_consumer_refresh_dashboard_handler, args = [topic, value])
        thread.start()
    except Exception as e:
        logger.error("Error while parsing request")
        logger.exception(e)
        return str(e), 400
    return '', 201    


if __name__ == "__main__":
    # Usage: /usr/bin/python3 kafka_consumer.py --dcs_dashboard_ip_port localhost:8080 --kafka_ip_port localhost:9092 --log info
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dcs_dashboard_ip_port",
        help='DCS Dashboard IP:port',
        default='localhost:8080')
    parser.add_argument(
        "--kafka_ip_port",
        help='Kafka IP:port',
        default='localhost:9092')
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
    logging.getLogger("KafkaConsumer").setLevel(numeric_level)
    logging.getLogger("requests.packages.urllib3").setLevel(logging.ERROR)

    global dcs_dashboard_ip_port 
    dcs_dashboard_ip_port = str(args.dcs_dashboard_ip_port)
    global url_dcs_dashboard
    url_dcs_dashboard = "http://" + dcs_dashboard_ip_port + "/portal/dcs/dashboard"

    global kafka_ip_port 
    kafka_ip_port= str(args.kafka_ip_port) 

    logger.info("Serving KafkaConsumer on port 8291")

    serve(app, host='0.0.0.0', port=8291)
