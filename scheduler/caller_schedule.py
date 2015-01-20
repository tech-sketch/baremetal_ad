#!/bin/env python

from schedule.rule.rule import Rule

class Schedule(object):

    def __init__(self, hostname):
        self.candidate_proxy = ""
        rule = Rule(host_name = hostname, api_url = "http://localhost/zabbix/api_jsonrpc.php", username = "Admin", password = "zabbix", filepath = "/usr/lib/zabbix/scheduler/schedule/conf/sample_rule.json")
        rule.read_definition()
        rule.check_current_settings()
        self.candidate_proxy = rule.candidate_proxy
