#!/bin/bash

# Not used in the current version. It is here in case of needing it.

source /etc/default/logstash
/usr/share/logstash/bin/logstash "--path.settings" "/etc/logstash" > /var/log/logstash.log &
#echo $! > /tmp/logstash.pid
ps aux | grep -i logstash | awk NR==1{'print $2'} > /tmp/logstash.pid
