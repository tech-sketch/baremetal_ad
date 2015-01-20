import json

from schedule.rule.ipmi_ip_rule import IpmiIpRule
from schedule.rule.host_num_rule import HostNumRule

class Rule(object):

    """
    Rule class is Abstract object class.
    """

    def __init__(self, host_name, api_url, username, password, filepath):
        self.host_name = host_name
        self.candidate_proxy = ""
        self.rule_definition = None
        self.api_url = api_url
        self.username = username
        self.password = password
        self.filepath = filepath
        self.rule_data = ""

    def read_definition(self):
        """
        ToDo
        """
        file = open(self.filepath, 'r')

        ruleData = json.load(file)
        keyList = ruleData.keys()
        keyList.sort()

        for group_name in keyList:
            self.rule_definition = group_name
            self.rule_data = ruleData[group_name]
            break

    def check_current_settings(self):
        """
        ToDo
        """
        if self.rule_definition == "ipmi_ip":
            print "IpmiIpRule execute!"
            rule = IpmiIpRule(self.host_name, self.api_url, self.username, self.password, self.rule_data)
            self.candidate_proxy = rule.suggest_candidate_proxy()
            rule.execute(self.candidate_proxy)
        elif self.rule_definition == "host_num":
            print "HostNumRule execute!"
            rule = HostNumRule(self.host_name, self.api_url, self.username, self.password)
            self.candidate_proxy = rule.suggest_candidate_proxy()
            rule.execute(self.candidate_proxy)
        elif self.rule_definition == "host_name":
            print "Please implement logic!"

