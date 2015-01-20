import json, urllib2

class ZabbixApi(object):

    def __init__(self, api_url, username, password):
        self.api_url = api_url
        self.username = username
        self.password = password

    def user_login(self):
        post = json.dumps({'jsonrpc':'2.0', 'method':'user.login', 'params':{'user':self.username, 'password':self.password}, 'auth':None, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        self.auth_token = contents_dict["result"]
        return True

    def create_proxy(self, proxy_name, mode, ipaddress, dns, type, port):
        if mode == 0:
            post = json.dumps({'jsonrpc':'2.0', 'method':'proxy.create', 'params':{'host':proxy_name, 'status': '5'},'auth': self.auth_token,'id':1})
        elif mode == 1:
            post = json.dumps({'jsonrpc':'2.0', 'method':'proxy.create', 'params':{'host':proxy_name, 'status': '6', 'interfaces': [{'ip':ipaddress, 'dns':dns, 'useip':type, 'port':port}]},'auth': self.auth_token,'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        return True

    def get_proxy_list(self):
        post = json.dumps({'jsonrpc':'2.0', 'method':'proxy.get', 'params':{'output':'extend', 'selectInterface':'extend'}, 'auth':self.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        proxy_list = []
        for i in range(len(contents_dict["result"])):
            proxy_list.append(contents_dict["result"][i]["host"])
        return proxy_list

    def attach_host_proxy(self, proxy_name, host_name):
        host_id = self._get_id('host', host_name)
        proxy_id = self._get_id('proxy', proxy_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'host.update', 'params':{'hostid':host_id, 'proxy_hostid':proxy_id},'auth': self.auth_token,'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)

        return True

    def detach_host_proxy(self, host_name):
        host_id = self._get_id('host', host_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'host.update', 'params':{'hostid':host_id, 'proxy_hostid':None},'auth': self.auth_token,'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)

        return True

    def reattach_host_proxy(self, new_proxy_name, host_name):
        host_id = self._get_id('host', host_name)
        proxy_id = self._get_id('proxy', proxy_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'host.update', 'params':{'hostid':host_id, 'proxy_hostid':proxy_id},'auth': self.auth_token,'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        return True

    def get_host_list(self):
        post = json.dumps({'jsonrpc':'2.0', 'method':'host.get', 'params':{'output':'extend'}, 'auth':self.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())

        host_list = []
        for i in range(len(contents_dict["result"])):
            host_list.append(contents_dict["result"][i]["name"])
        return host_list

    def get_attached_host_list(self, proxy_name):
        proxy_id = self._get_id('proxy', proxy_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'host.get', 'params':{'output':'extend', 'filter':{'proxy_hostid': proxy_id}}, 'auth':self.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())

        host_list = []
        for i in range(len(contents_dict["result"])):
            host_list.append(contents_dict["result"][i]["name"])
        return host_list

    def get_interface_ipaddress(self, host_name, type):
        host_id = self._get_id('host', host_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'hostinterface.get', 'params':{'output':'extend','hostids':host_id, 'filter':{'type': type}}, 'auth':self.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        ipaddress = contents_dict["result"][0]["ip"]
        return ipaddress

    def get_host_proxy(self, host_name):
        host_id = self._get_id('host', host_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'host.get', 'params':{'output':'extend', 'filter':{'host': host_name}}, 'auth':self.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        proxy_id = contents_dict["result"][0]["proxy_hostid"]

        post = json.dumps({'jsonrpc':'2.0', 'method':'proxy.get', 'params':{'output':'extend', 'selectInterface':'extend', 'filter':{'proxyid': proxy_id}}, 'auth':self.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        proxy_name = contents_dict["result"][0]["host"]
        return proxy_name

    def set_ipmi_setting(self, host_name, authtype, privilege, ipmi_password, ipmi_user_name):
        host_id = self._get_id('host', host_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'host.update', 'params':{'hostid':host_id, 'ipmi_authtype':authtype, 'ipmi_privilege':privilege, 'ipmi_password':ipmi_password, 'ipmi_username':ipmi_user_name}, 'auth':self.auth_token, 'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        return True

    def get_lastvalue(self, host_name, key):
        host_id = self._get_id('host', host_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'item.get', 'params':{'output':'extend', 'hostids':host_id, 'search':{'key_':key}}, 'auth':self.auth_token, 'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        lastvalue = contents_dict["result"][0]["lastvalue"]
        return lastvalue

    def create_host_interface(self, host_name, dns, ipaddress, main, port, type, useip):
        host_id = self._get_id('host', host_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'hostinterface.create', 'params':{'hostid':host_id, 'dns':dns, 'ip':ipaddress, 'main':main, 'port':port, 'type':type, 'useip':useip}, 'auth':self.auth_token, 'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        return True

    def delete_host_interface(self, host_name):
        host_id = self._get_id('host', host_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'hostinterface.get', 'params':{'output':'extend','hostids':host_id, 'filter':{'type': '1'}}, 'auth':self.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())

        for i in range(len(contents_dict["result"])):
            interface_id = contents_dict["result"][i]["interfaceid"]
            post = json.dumps({'jsonrpc':'2.0', 'method':'hostinterface.delete', 'params':[interface_id],'auth': self.auth_token,'id':1})
            request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
            contents = urllib2.urlopen(request)
        return True

    def attach_host_group(self, host_name, group_name):
        host_id = self._get_id('host', host_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'hostgroup.get', 'params':{'output':'extend', 'filter':{"name":[group_name]}}, 'auth':self.auth_token, 'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        group_id = contents_dict["result"][0]["groupid"]
        post = json.dumps({'jsonrpc':'2.0', 'method':'hostgroup.massadd', 'params':{'groups':[{'groupid':group_id}], 'hosts':[{'hostid': host_id}]}, 'auth':self.auth_token, 'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        return True

    def attach_templates(self, host_name, template_name):
        host_id = self._get_id('host', host_name)
        template_id = self._get_id('template', template_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'template.massadd', 'params':{'templates':[{'templateid':template_id}], 'hosts':[{'hostid':host_id}]}, 'auth':self.auth_token, 'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        return True

    def detach_templates(self, host_name, template_name):
        host_id = self._get_id('host', host_name)
        template_id = self._get_id('template', template_name)
        post = json.dumps({'jsonrpc':'2.0', 'method':'host.update', 'params':{'hostid':host_id, 'templates_clear':[{'templateid': template_id}]}, 'auth':self.auth_token, 'id':1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        return True

    def _get_id(self, name, host):
        method = name + '.get'
        id = name + 'id'
        post = json.dumps({'jsonrpc':'2.0', 'method':method, 'params':{'output':'extend', 'filter':{'host': [host]}}, 'auth':self.auth_token, 'id': 1})
        request = urllib2.Request(self.api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        return contents_dict["result"][0][id]
