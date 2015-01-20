import commands

from common.zabbix_api import ZabbixApi
from caller_schedule import Schedule

class ZabbixAction(object):

    def __init__(self, host_name, ipaddress, api_url, username, password):
        self.host_name = host_name
        self.ipaddress = ipaddress
        self.api_url = api_url
        self.username = username
        self.password = password
        self.path = "/usr/lib/zabbix/scheduler"

    def IpmiInterfaces(self):
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        self.ipaddress = api.get_lastvalue(self.host_name, 'ssh.run[dcmi]')
        api.create_host_interface(self.host_name, '', self.ipaddress, 1, '623', 3, 1)
        api.set_ipmi_setting(self.host_name, -1, 4, "admin", "admin")
        api.attach_host_group(self.host_name, "OCP Servers")

        product_name = commands.getoutput('ipmitool -I lanplus -H ' + self.ipaddress + ' -U ' + 'admin' + ' -P ' + 'admin' + ' -A MD5 fru | grep "Product Name" | cut -d: -f2 | tr -d " "')
        api.attach_templates(self.host_name, 'Template OCP ' + product_name)

        schedule = Schedule(self.host_name)
        proxy_name = schedule.candidate_proxy

        print proxy_name
        if proxy_name != '':
            agent_ipaddress = api.get_interface_ipaddress(self.host_name, '1')
            proxy_ipaddress = api.get_interface_ipaddress(proxy_name, '1')
            commands.getoutput("/bin/sh " + self.path + "/action/update_agent_conf.sh " + agent_ipaddress + " " + proxy_ipaddress)

        api.detach_templates(self.host_name, 'Template SSH Agent')
        api.delete_host_interface(self.host_name)

    def AgentInterfaces(self):
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        api.create_host_interface(self.host_name, '', self.ipaddress, 1, '10050', 1, 1)

        os_name = commands.getoutput('zabbix_get -s ' + self.ipaddress + ' -k system.sw.os | cut -d" " -f1')
        api.attach_templates(self.host_name, 'Custom Template OS ' + os_name)
        api.attach_templates(self.host_name, 'Template Screen')
        proxy_name = api.get_host_proxy(self.host_name)

        if proxy_name != '':
            agent_ipaddress = api.get_interface_ipaddress(self.host_name, '1')
            proxy_ipaddress = api.get_interface_ipaddress(proxy_name, '1')
            commands.getoutput("/bin/sh " + self.path + "/action/update_agent_conf.sh " + agent_ipaddress + " " + proxy_ipaddress)

    def CreateProxy(self):
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        proxy_name = api.get_lastvalue(self.host_name, 'proxy.name')
        api.create_proxy(proxy_name,'0','','','','')
