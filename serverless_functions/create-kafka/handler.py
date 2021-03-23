from kafka.admin import KafkaAdminClient, NewTopic
import json

def handle(event, context):
    if event.method == 'POST':
        data = json.loads(event.body)
        if "topic" not in data:
            return {
                "statusCode": 400,
                "body": "Format not valid"
            }
        try:
            topic = data["topic"]
            admin_client = KafkaAdminClient(bootstrap_servers="kafka.deployment8:9092", client_id='create_kafka_topic')
            topic_list = []
            topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            admin_client.close()
        except Exception as e:
            return {
                "statusCode": 400,
                "body": "".format(e)
            }
        return {
            "statusCode": 200,
            "body": "OK"
        }
    else:
        return {
            "statusCode": 200,
            "body": "No action for this endpoint"
        }

