import requests
import argparse
import logging
import coloredlogs
from flask import Flask, request, jsonify
from flask_swagger import swagger
from waitress import serve
from kafka import KafkaConsumer
import json


app = Flask(__name__)
logger = logging.getLogger("FetchKafkaTopic")


@app.route('/', methods=['GET'])
def server_status():
    logger.info("GET /")
    return '', 200


@app.route("/spec", methods=['GET'])
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "FetchKafkaTopic REST API"
    return jsonify(swag)


@app.route("/fetch_kafka_topic", methods=['GET'])
def fetch_kafka_topic():
    logger.info("Request received - GET /fetch_kafka_topic")
    output = 404

    if not request.is_json:
        logger.warning("Format not valid")
        return 'Format not valid', 400
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=[kafka_ip_port],
            client_id='fetch_kafka_topic')

        # Parse JSON
        data = request.get_json()
        logger.info("Data received: %s", data)
        topic = data["topic"]

        logger.info("Checking if topic %s exists in Kafka", topic)

        kafka_topics = consumer.topics()
        if topic in kafka_topics:
            output = 302
        else:
            output = 404
        consumer.close()
    except Exception as e:
        logger.error("Error while parsing request")
        logger.exception(e)
        return str(e), 400
    return '', output


if __name__ == "__main__":
    # Usage: /usr/bin/python3 fetch_kafka_topic.py --kafka_ip_port localhost:9092 --log info
    parser = argparse.ArgumentParser()
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
    logging.getLogger("FetchKafkaTopic").setLevel(numeric_level)
    logging.getLogger("requests.packages.urllib3").setLevel(logging.ERROR)

    global kafka_ip_port 
    kafka_ip_port= str(args.kafka_ip_port) 

    logger.info("Serving FetchKafkaTopic on port 8390")
    serve(app, host='0.0.0.0', port=8390)
