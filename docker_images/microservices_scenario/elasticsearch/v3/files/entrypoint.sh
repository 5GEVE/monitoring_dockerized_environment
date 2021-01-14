#!/bin/bash

# Start Elasticsearch
/etc/init.d/elasticsearch start
sleep 2
tail -f /var/log/elasticsearch/dcs.log

