import requests
import argparse
import logging
import coloredlogs
from flask import Flask, request, jsonify
from flask_swagger import swagger
from waitress import serve
import subprocess
import json


app = Flask(__name__)
logger = logging.getLogger("LogstashPipelineManager")


@app.route('/', methods=['GET'])
def server_status():
    logger.info("GET /")
    return '', 200


@app.route("/spec", methods=['GET'])
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "LogstashPipelineManager REST API"
    return jsonify(swag)


@app.route('/logstash_pipeline_manager', methods=['POST'])
def create_logstash_pipeline():
    logger.info("Request received - POST /logstash_pipeline_manager")
    if not request.is_json:
        logger.warning("Format not valid")
        return 'Format not valid', 400
    try:
        # Parse JSON
        data = request.get_json()
        logger.info("Data received: %s", data)
        topic = data["topic"]

        logger.info("Create Logstash pipeline for topic %s", topic)
        subprocess.call(['/bin/bash', script_path + '/create_logstash_pipeline.sh', topic, elasticsearch_ip_port, kafka_ip_port, elk_password])
    except Exception as e:
        logger.error("Error while parsing request")
        logger.exception(e)
        return str(e), 400
    return '', 201
                        

@app.route('/logstash_pipeline_manager', methods=['DELETE'])
def delete_logstash_pipeline():
    logger.info("Request received - DELETE /logstash_pipeline_manager")
    if not request.is_json:
        logger.warning("Format not valid")
        return 'Format not valid', 400
    try:
        # Parse JSON
        data = request.get_json()
        logger.info("Data received: %s", data)
        topic = data["topic"]

        logger.info("Delete Logstash pipeline for topic %s", topic)
        subprocess.call(['/bin/bash', script_path + '/delete_logstash_pipeline.sh', topic])
    except Exception as e:
        logger.error("Error while parsing request")
        logger.exception(e)
        return str(e), 400
    return '', 201


if __name__ == "__main__":
    # Usage: /usr/bin/python3 logstash_pipeline_manager.py --script_path /tmp --kafka_ip_port localhost:9092 --elasticsearch_ip_port localhost:9200 --elk_password changeme --log info
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--script_path",
        help='Script path')
    parser.add_argument(
        "--kafka_ip_port",
        help='Kafka IP:port',
        default='localhost:9092')
    parser.add_argument(
        "--elasticsearch_ip_port",
        help='Elasticsearch IP:port',
        default='localhost:9200')
    parser.add_argument(
        "--elk_password",
        help='ELK password')
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
    logging.getLogger("LogstashPipelineManager").setLevel(numeric_level)
    logging.getLogger("requests.packages.urllib3").setLevel(logging.ERROR)

    global script_path 
    script_path= str(args.script_path) 
    
    global kafka_ip_port 
    kafka_ip_port= str(args.kafka_ip_port) 

    global elasticsearch_ip_port 
    elasticsearch_ip_port = str(args.elasticsearch_ip_port)    
    global url_elasticsearch
    url_elasticsearch = "http://" + elasticsearch_ip_port

    global elk_password
    elk_password= str(args.elk_password)

    logger.info("Serving LogstashPipelineManager on port 8191")

    serve(app, host='0.0.0.0', port=8191)
