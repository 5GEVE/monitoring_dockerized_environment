import requests
import argparse
import logging
import coloredlogs
import threading
from flask import Flask, request, jsonify
from flask_swagger import swagger
from waitress import serve
import json
from threading import Thread
from threading import Timer
from datetime import timedelta
#import psycopg2
import time


app = Flask(__name__)
logger = logging.getLogger("DCSRestClient")


@app.route('/', methods=['GET'])
def server_status():
    logger.info("GET /")
    return '', 200


@app.route("/spec", methods=['GET'])
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "DCS REST API"
    return jsonify(swag)


def create_elasticsearch_index(topic):
    logger.info("Creating Elasticsearch index for topic %s (in lowercase)", topic)
    r = requests.put(url_elasticsearch + "/" + topic, auth=('elastic', elk_password))
    logger.info("Response: Code %s", r)


def create_logstash_pipeline(topic):
    logger.info("Creating Logstash pipeline for topic %s", topic)
    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.post(url_logstash_pipeline_manager, json=request_body)
    logger.info("Response: Code %s", r)


def kafka_consumer(value):
    logger.info("Creating Kafka consumer for value %s", value)
    request_body = json.loads(json.dumps({'value': value}))
    r = requests.post(url_kafka_consumer, json=request_body)
    logger.info("Response: Code %s", r)


@app.route('/portal/dcs/subscribe', methods=['POST'])
def subscribe():
    logger.info("Request received - POST /portal/dcs/subscribe")
    if not request.is_json:
        logger.warning("Format not valid")
        return 'Format not valid', 400
    try:
        data = request.get_json()
        value = data["value"]
        topic = value["topic"]

        # Create Elasticsearch index
        create_elasticsearch_index(topic.lower())

        # Create Logstash pipeline
        create_logstash_pipeline(topic)

        # Create Kafka consumer to wait for the first message received in the topic and, then, refresh the dashboard.
        kafka_consumer(value)

        # Finally, save topic in DB
        #try:
            #connection = psycopg2.connect(user = "eve", password = eve_db_password, host = db_ip, port = "5432", dbname="pipelines")
            #logger.info("Inserting %s topic in database", topic)
            #cursor = connection.cursor()
            #cursor.execute("INSERT INTO pipeline VALUES ( %s )", (topic,))
            #connection.commit()
            #logger.info("Topic %s inserted in database", topic)
            #cursor.close()
            #connection.close()
        #except (Exception, psycopg2.Error) as error:
            #logger.error("Error while connecting to PostgreSQL: ", error)
    except Exception as e:
        logger.error("Error while parsing request")
        logger.exception(e)
        return str(e), 400
    return '', 201


def delete_logstash_pipeline(topic):
    logger.info("Deleting Logstash pipeline for topic %s", topic)
    request_body = json.loads(json.dumps({'topic': topic}))
    r = requests.delete(url_logstash_pipeline_manager, json=request_body)
    logger.info("Response: Code %s", r)


def index_cleaner(topic, value):

    logger.info("Time to delete the dashboard for topic %s", topic)
    r_first = requests.delete(url_dcs_dashboard, json=json.loads(json.dumps({'records': [ { 'value': value }]})))
    logger.info("Response: Code %s", r_first)

    logger.info("Time to delete the Elasticsearch index for topic %s", topic)
    r_second = requests.delete(url_elasticsearch + "/" + topic, auth=('elastic', elk_password))
    logger.info("Response: Code %s", r_second)


@app.route('/portal/dcs/unsubscribe', methods=['DELETE'])
def unsubscribe():
    logger.info("Request received - DELETE /portal/dcs/unsubscribe")
    if not request.is_json:
        logger.warning("Format not valid")
        return 'Format not valid', 400
    try:
        data = request.get_json()
        value = data["value"]
        topic = value["topic"]

        # Delete Logstash pipeline
        delete_logstash_pipeline(topic)
                        
        # Schedule the removal of Kibana dashboard and Elasticsearch index (30 seconds)
        scheduled_thread = threading.Timer(timedelta(seconds=30).total_seconds(), index_cleaner, args = [topic.lower(), value])
        scheduled_thread.start()
        logger.info("Data removal for topic %s scheduled in 30 seconds", topic)

        # Finally, delete topic in DB
        #try:
            #connection = psycopg2.connect(user = "eve", password = eve_db_password, host = db_ip, port = "5432", dbname="pipelines")
            #logger.info("Deleting %s topic in database", topic)
            #cursor = connection.cursor()
            #cursor.execute("DELETE FROM pipeline WHERE topic = %s", (topic,))
            #connection.commit()
            #logger.info("Topic %s deleted in database", topic)
            #cursor.close()
            #connection.close()
        #except (Exception, psycopg2.Error) as error:
            #logger.error("Error while connecting to PostgreSQL: ", error)
    except Exception as e:
        logger.error("Error while parsing request")
        logger.exception(e)
        return str(e), 400
    return '', 201


if __name__ == "__main__":
    # Usage: /usr/bin/python3 dcs_rest_client.py --dcs_dashboard_ip_port localhost:8080 --logstash_pipeline_manager_ip_port localhost:8191 --kafka_consumer_ip_port localhost:8291 --elasticsearch_ip_port localhost:9200 --elk_password changeme --db_ip localhost --eve_db_password changeme --log info
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dcs_dashboard_ip_port",
        help='DCS Dashboard IP:port',
        default='localhost:8080')
    parser.add_argument(
        "--logstash_pipeline_manager_ip_port",
        help='logstashPipelineManager service IP:port',
        default='localhost:8191')
    parser.add_argument(
        "--kafka_consumer_ip_port",
        help='kafkaConsumer function IP:port',
        default='localhost:8291')
    parser.add_argument(
        "--elasticsearch_ip_port",
        help='Elasticsearch IP:port',
        default='localhost:9200')
    parser.add_argument(
        "--elk_password",
        help='ELK password')
    #parser.add_argument(
        #"--db_ip",
        #help='DB IP address',
        #default='localhost')
    #parser.add_argument(
        #"--eve_db_password",
        #help='DB password for eve user')
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
    logging.getLogger("DCSRestClient").setLevel(numeric_level)
    logging.getLogger("requests.packages.urllib3").setLevel(logging.ERROR)

    global dcs_dashboard_ip_port 
    dcs_dashboard_ip_port = str(args.dcs_dashboard_ip_port)
    global url_dcs_dashboard
    url_dcs_dashboard = "http://" + dcs_dashboard_ip_port + "/portal/dcs/dashboard"

    global logstash_pipeline_manager_ip_port 
    logstash_pipeline_manager_ip_port = str(args.logstash_pipeline_manager_ip_port)
    global url_logstash_pipeline_manager
    url_logstash_pipeline_manager = "http://" + logstash_pipeline_manager_ip_port + "/logstash_pipeline_manager"
    
    global kafka_consumer_ip_port
    kafka_consumer_ip_port = str(args.kafka_consumer_ip_port)
    global url_kafka_consumer
    url_kafka_consumer = "http://" + kafka_consumer_ip_port + "/kafka_consumer"
    
    global elasticsearch_ip_port 
    elasticsearch_ip_port = str(args.elasticsearch_ip_port)    
    global url_elasticsearch
    url_elasticsearch = "http://" + elasticsearch_ip_port

    global elk_password
    elk_password= str(args.elk_password)
    #global db_ip
    #db_ip= str(args.db_ip)
    #global eve_db_password
    #eve_db_password= str(args.eve_db_password)

    logger.info("Serving DCSRestClient on port 8091")

    serve(app, host='0.0.0.0', port=8091)
