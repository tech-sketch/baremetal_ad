#!/bin/env python

# Run when the ZabbixServer was initially installed
#
# Usages:
#
#   caller_server
#

import sys, commands

from server_startup.zabbix_server_startup import ZabbixServerStartUp

if __name__ == "__main__":
    server = ZabbixServerStartUp(api_url = "http://localhost/zabbix/api_jsonrpc.php", username = "Admin", password = "zabbix")
    print "Zabbix-Server StartUp execute!"
    server.GetServerHost()
    server.HostStatusChange()
    server.CreateTemplates()
    server.CreateAction()
    print "Finish!"
