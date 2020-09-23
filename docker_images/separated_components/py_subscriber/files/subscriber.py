import json
from kafka import KafkaConsumer
import sys

# usage: python3 subscriber.py {broker_ip_address}:{port} {topic}
# e.g.   python3 subscriber.py 192.168.11.51:9093 uc.4.france_nice.infrastructure_metric.expb_metricId

consumer = KafkaConsumer(sys.argv[2], bootstrap_servers=[sys.argv[1]], auto_offset_reset='earliest', enable_auto_commit=True, group_id=None, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
check = True
while check:
    message = consumer.poll(timeout_ms=1000)
    if message != {}:
        print("Message received in %s topic: %s", sys.argv[2], message)
        for tp, messages in message.items():
            for msg in messages:
                print("Value: %s", msg.value)
