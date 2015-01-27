import sys, json, urllib2, commands

def user_login(username, password, api_url):
    post = json.dumps({'jsonrpc':'2.0', 'method':'user.login', 'params':{'user':username, 'password':password}, 'auth':None, 'id': 1})
    request = urllib2.Request(api_url, post, {"Content-Type":"application/json-rpc"})
    contents = urllib2.urlopen(request)
    contents_dict = json.loads(contents.read())
    auth_token = contents_dict["result"]
    return auth_token

def get_host_proxy(host_name, auth_token, api_url):
    host_id = get_id('host', host_name, auth_token, api_url)
    post = json.dumps({'jsonrpc':'2.0', 'method':'host.get', 'params':{'output':'extend', 'filter':{'host': host_name}}, 'auth':auth_token, 'id': 1})
    request = urllib2.Request(api_url, post, {"Content-Type":"application/json-rpc"})
    contents = urllib2.urlopen(request)
    contents_dict = json.loads(contents.read())
    proxy_id = contents_dict["result"][0]["proxy_hostid"]

    proxy_name = ""
    if proxy_id != "0":
        post = json.dumps({'jsonrpc':'2.0', 'method':'proxy.get', 'params':{'output':'extend', 'selectInterface':'extend', 'filter':{'proxyid': proxy_id}}, 'auth':auth_token, 'id': 1})
        request = urllib2.Request(api_url, post, {"Content-Type":"application/json-rpc"})
        contents = urllib2.urlopen(request)
        contents_dict = json.loads(contents.read())
        proxy_name = contents_dict["result"][0]["host"]
    return proxy_name

def get_interface_ipaddress(host_name, type, auth_token, api_url):
    host_id = get_id('host', host_name, auth_token, api_url)
    post = json.dumps({'jsonrpc':'2.0', 'method':'hostinterface.get', 'params':{'output':'extend','hostids':host_id, 'filter':{'type': type}}, 'auth':auth_token, 'id': 1})
    request = urllib2.Request(api_url, post, {"Content-Type":"application/json-rpc"})
    contents = urllib2.urlopen(request)
    contents_dict = json.loads(contents.read())
    ipaddress = contents_dict["result"][0]["ip"]
    return ipaddress

def get_id(name, host, auth_token, api_url):
    method = name + '.get'
    id = name + 'id'
    post = json.dumps({'jsonrpc':'2.0', 'method':method, 'params':{'output':'extend', 'filter':{'host': [host]}}, 'auth':auth_token, 'id': 1})
    request = urllib2.Request(api_url, post, {"Content-Type":"application/json-rpc"})
    contents = urllib2.urlopen(request)
    contents_dict = json.loads(contents.read())
    return contents_dict["result"][0][id]

if __name__ == "__main__":
    server_ip = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    host_name = sys.argv[4]
    ipaddress = sys.argv[5]
    api_url = "http://"+ server_ip +"/zabbix/api_jsonrpc.php"
    auth_token = user_login(username, password, api_url)
    proxy_name = get_host_proxy(host_name, auth_token, api_url)
    if proxy_name != "":
        connect_ipaddress = get_interface_ipaddress(proxy_name, '1', auth_token, api_url)
        commands.getoutput("zabbix_sender -vv -z " + connect_ipaddress + " -s " + host_name + " -k \"agent.ip\" -o "+ ipaddress)
        commands.getoutput("sed -i -e \"s/^Server=.*/Server="+ server_ip +"," + connect_ipaddress +"/g\" /etc/zabbix/zabbix_agentd.conf")
        commands.getoutput("sed -i -e \"s/^ServerActive=.*/ServerActive="+ connect_ipaddress +"/g\" /etc/zabbix/zabbix_agentd.conf")
    else:
        connect_ipaddress = server_ip
        commands.getoutput("zabbix_sender -vv -z " + connect_ipaddress + " -s " + host_name + " -k \"agent.ip\" -o "+ ipaddress)
