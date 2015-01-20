#!/bin/env python
import sys

from action.zabbix_action import ZabbixAction

if __name__ == "__main__":
    if sys.argv[1] == "UpdateIpmiInterfaces":
        print "Update IPMI interfaces execute!"
        action = ZabbixAction(host_name = sys.argv[2], ipaddress = "",  api_url = "http://localhost/zabbix/api_jsonrpc.php", username = "Admin", password = "zabbix")
        action.IpmiInterfaces()
    elif sys.argv[1] == "UpdateAgentInterfaces":
        print "Update Agent interfaces execute!"
        action = ZabbixAction(host_name = sys.argv[2], ipaddress = sys.argv[3], api_url = "http://localhost/zabbix/api_jsonrpc.php", username = "Admin", password = "zabbix")
        action.AgentInterfaces()
    elif sys.argv[1] == "CreateProxy":
        print "Create Proxy execute!"
        action = ZabbixAction(host_name = sys.argv[2], ipaddress = "", api_url = "http://localhost/zabbix/api_jsonrpc.php", username = "Admin", password = "zabbix")
        action.CreateProxy()
    print "Finish!"
