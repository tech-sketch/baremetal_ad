from schedule.schedule.host_num_schedule import HostNumSchedule
from common.zabbix_api import ZabbixApi

class HostNumRule(object):
    """
    Controlled host number based Rule class
    """
    def __init__(self, host_name, api_url, username, password):
        self.host_name = host_name
        self.api_url = api_url
        self.username = username
        self.password = password

    def suggest_candidate_proxy(self):
        """
        ToDo
        """
        api = ZabbixApi(self.api_url, self.username, self.password)
        api.user_login()
        proxies = api.get_proxy_list()
        host_count = {}
        for i in range(len(proxies)):
            host_list = api.get_attached_host_list(proxies[i])
            host_count[proxies[i]] = len(host_list)
            print host_list
            print host_count[proxies[i]]
            print host_count
        candidate_proxy = min(host_count, key=(lambda x: host_count[x]))
        print "Proxy: %s" % candidate_proxy
        return candidate_proxy

    def execute(self, candidate_proxy):
        schedule = HostNumSchedule(self.host_name, candidate_proxy, self.api_url, self.username, self.password)
        schedule.attach_proxy()

