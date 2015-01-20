from schedule.schedule.ipmi_ip_schedule import IpmiIpSchedule
from common.zabbix_api import ZabbixApi

class IpmiIpRule(object):
    """
    IPMI IP address based Rule class
    """
    def __init__(self, host_name, api_url, username, password, rule_data):
        self.host_name = host_name
        self.api_url = api_url
        self.username = username
        self.password = password
        self.rule_data = rule_data

    def suggest_candidate_proxy(self):
        """
        ToDo
        """
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        proxies = api.get_proxy_list()

        ipmi_ip = api.get_interface_ipaddress(self.host_name, '3')
        setting = self.rule_data
        proxy_name = ''
        for j in setting:
            flag = ''
            if proxy_name != '':
                break
            for i in [0, 1, 2, 3]:
                ip = int(ipmi_ip.split(".")[i])
                from_ip = int(setting[j]["from"].split(".")[i])
                to_ip = int(setting[j]["to"].split(".")[i])
                if flag == 'from' and from_ip < ip:
                    proxy_name = j
                    break
                elif flag == 'from' and from_ip == ip:
                    if i == 3:
                        proxy_name = j
                        break
                    else:
                        flag == 'from'
                        continue
                elif flag == 'from' and from_ip > ip:
                    break
                elif flag == 'to' and to_ip < ip:
                    break
                elif flag == 'to' and to_ip == ip:
                    if i == 3:
                        proxy_name = j
                        break
                    else:
                        flag == 'to'
                        continue
                elif flag == 'to' and to_ip > ip:
                    proxy_name = j
                    break
                elif i == 3 and ip == to_ip:
                    proxy_name = j
                    break
                elif i == 3 and ip == from_ip:
                    proxy_name = j
                    break
                elif from_ip == to_ip and to_ip == ip:
                    continue
                elif from_ip < to_ip and from_ip == ip:
                    flag = 'from'
                    continue
                elif from_ip < to_ip and to_ip == ip:
                    flag = 'to'
                    continue
                elif from_ip < ip and ip < to_ip:
                    proxy_name = j
                    break
                else:
                    break
        candidate_proxy = proxy_name
        print "Proxy: %s" % candidate_proxy
        return proxy_name

    def execute(self, candidate_proxy):
        schedule = IpmiIpSchedule(self.host_name, candidate_proxy, self.api_url, self.username, self.password)
        schedule.attach_proxy()


