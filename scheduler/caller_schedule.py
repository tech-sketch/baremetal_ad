#!/bin/env python

# Run when the Proxy schedule
#
# Usages:
#
#   caller_schedule <hostname>
#
import os.path
from schedule.rule.rule import Rule

class Schedule(object):

    def __init__(self, hostname):
        self.candidate_proxy = ''
        path = "/usr/lib/zabbix/scheduler/schedule/conf/proxy_rule.json"
        if os.path.exists(path):
            rule = Rule(host_name = hostname, api_url = "http://localhost/zabbix/api_jsonrpc.php", username = "Admin", password = "zabbix", filepath = path)
            rule.read_definition()
            rule.check_current_settings()
            self.candidate_proxy = rule.candidate_proxy
