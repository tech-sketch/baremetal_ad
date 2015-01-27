import json, urllib2, commands

from common.zabbix_api import ZabbixApi

class ZabbixServerStartUp(object):

    def __init__(self, api_url, username, password):
        self.host_name = ""
        self.api_url = api_url
        self.username = username
        self.password = password
        self.path = "/usr/lib/zabbix/scheduler"

    def GetServerHost(self):
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        host_list = api.get_host_list()
        self.host_name = host_list[0]

    def HostStatusChange(self):
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        api.host_status_change(self.host_name, 0)

    def CreateTemplates(self):
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        templates = open("/usr/lib/zabbix/template/zbx_export_templates.xml").read()
        post = json.dumps({'jsonrpc':'2.0', 'method':'configuration.import', 'params':{'format': 'xml','rules': {'groups': {'createMissing': 'true'},'templates': {'createMissing': 'true','updateExisting': 'true'},'templateScreens': {'createMissing': 'true','updateExisting': 'true'},'templateLinkage': {'createMissing': 'true'},'applications': {'createMissing': 'true'},'items': {'createMissing': 'true','updateExisting': 'true'},'discoveryRules': {'createMissing': 'true','updateExisting': 'true'},'triggers': {'createMissing': 'true','updateExisting': 'true'},'graphs': {'createMissing': 'true','updateExisting': 'true'}},'source': templates},'auth': api.auth_token,'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)

    def CreateAction(self):
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()

        post = json.dumps({'jsonrpc':'2.0', 'method':'host.get', 'params':{'output':'extend', 'filter':{'host': [self.host_name]}}, 'auth':api.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        host_id =  contents_dict["result"][0]["hostid"]

        post = json.dumps({'jsonrpc':'2.0', 'method':'template.get', 'params':{'output':'extend', 'filter':{'host': "Template SSH Agent"}}, 'auth':api.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        template_id =  contents_dict["result"][0]["templateid"]

        post = json.dumps({'jsonrpc':'2.0', 'method':'action.create', 'params':{'name':'OCP STARTER Automatic Registration', 'eventsource':2, 'status':0, 'esc_period':0,'filter':{'evaltype': 0,'conditions': [{'conditiontype': 24,'operator': 2,'value': 'OCP STARTER'}]},'operations':[{"operationtype": 2},{'operationtype': 6,'optemplate': [{'templateid': template_id}]}]},'auth': api.auth_token,'id':1})
        request = urllib2.Request(api.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)

        post = json.dumps({'jsonrpc':'2.0', 'method':'action.create', 'params':{'name':'Create Proxy Action', 'eventsource':0, 'evaltype':0, 'status':0, 'esc_period':3600,'filter':{'evaltype': 1,'conditions': [{'conditiontype': 5,'operator': 0,'value': '1'},{'conditiontype': 3,'operator': 2,'value': 'Create Proxy Triggers'}]},'operations':[{'operationtype': 1,'esc_step_from': 1,'esc_step_to': 1,'evaltype': 1,'opcommand_hst': [{'hostid': '0'}],'opcommand': {'type': 0,'execute_on': 1,'command': '/usr/bin/python '+ self.path + '/caller_action.py "CreateProxy" "{HOST.NAME}"'}}]},'auth': api.auth_token,'id':1})
        request = urllib2.Request(api.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)

        post = json.dumps({'jsonrpc':'2.0', 'method':'action.create', 'params':{'name':'Update IPMI interfaces Action', 'eventsource':0, 'evaltype':0, 'status':0, 'esc_period':3600,'filter':{'evaltype': 1,'conditions': [{'conditiontype': 5,'operator': 0,'value': '1'},{'conditiontype': 3,'operator': 2,'value': 'SSH Triggers'}]},'operations':[{'operationtype': 1,'esc_step_from': 1,'esc_step_to': 1,'evaltype': 1,'opcommand_hst': [{'hostid': '0'}],'opcommand': {'type': 0,'execute_on': 1,'command': '/usr/bin/python ' + self.path + '/caller_action.py "UpdateIpmiInterfaces" "{HOST.NAME}"'}}]},'auth': api.auth_token,'id':1})
        request = urllib2.Request(api.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)

        post = json.dumps({'jsonrpc':'2.0', 'method':'action.create', 'params':{'name':'Update Agent interfaces Action', 'eventsource':0, 'evaltype':0, 'status':0, 'esc_period':3600,'filter':{'evaltype': 1,'conditions': [{'conditiontype': 5,'operator': 0,'value': '1'},{'conditiontype': 3,'operator': 2,'value': 'Update Agent interfaces Triggers'}]},'operations':[{'operationtype': 1,'esc_step_from': 1,'esc_step_to': 1,'evaltype': 1,'opcommand_hst': [{'hostid': '0'}],'opcommand': {'type': 0,'execute_on': 1,'command': '/usr/bin/python ' + self.path + '/caller_action.py "UpdateAgentInterfaces" "{HOST.NAME}"'}}]},'auth': api.auth_token,'id':1})
        request = urllib2.Request(api.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
