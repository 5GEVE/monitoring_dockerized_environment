#!/bin/bash
ip=$1
hostname=$2

echo "$ip $hostname" | tee -a /etc/hosts > /dev/null
