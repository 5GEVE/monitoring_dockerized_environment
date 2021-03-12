from kafka import KafkaConsumer
import json

def handle(event, context):
    if event.method == 'GET':
        data = json.loads(event.body)
        if "topic" not in data:
            return {
                "statusCode": 400,
                "body": "Format not valid"
            }
        try:
            topic = data["topic"]
            consumer = KafkaConsumer(bootstrap_servers=["kafka.deployment8:9092"], client_id='fetch_kafka_topic')
            kafka_topics = consumer.topics()
            if topic in kafka_topics:
                code = 302
            else:
                code = 404
            consumer.close()
        except Exception as e:
            return {
                "statusCode": 400,
                "body": "".format(e)
            }
        return {
            "statusCode": code,
            "body": "Done"
        }
    else:
        return {
            "statusCode": 200,
            "body": "No action for this endpoint"
        }
