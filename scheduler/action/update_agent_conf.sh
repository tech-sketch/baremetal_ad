#!/bin/sh

agent_ipaddress=$1
server_ipaddress=`ip -f inet -o addr show eth0|cut -d\  -f 7 | cut -d/ -f 1`
proxy_ipaddress=$2

zabbix_get -s $agent_ipaddress -k system.run["sed -i -e \"s/^Server=.*/Server="$server_ipaddress"\\\x2C"$proxy_ipaddress"/g\" /etc/zabbix/zabbix_agentd.conf"]
zabbix_get -s $agent_ipaddress -k system.run["sed -i -e \"s/^ServerActive=.*/ServerActive="$proxy_ipaddress"/g\" /etc/zabbix/zabbix_agentd.conf"]
zabbix_get -s $agent_ipaddress -k system.run["sed -i -e \"s/^HostMetadata=.*/HostMetadata=/g\" /etc/zabbix/zabbix_agentd.conf"]

zabbix_get -s $agent_ipaddress -k system.run["service zabbix-agent restart",nowait]
