Baremetal AutoDiscovery Tool for Zabbix
====

#Overview

Baremetal AutoDiscovery Tool for Zabbix(baremetal_ad) is an Apache2 Licensed, full baremetal monitoring tools, for OpenComputingProject(OCP) machine

#Description

- baremetal_ad to use zabbix-agent/ipmitool on the server monitoring
- <span style="color:red;">We created the ability to auto allocation in a Zabbix Proxy for ZabbixHost</span>
- automatically will be performed installation and monitoring, when you use MiniOS (Ubuntu Server 14.04) and a cobbler configuration file.
- Following monitoring will be performed automatically.
  - DCMI Monitoring
  - OS Monitoring
    - Linux OS
    - Mac OS
    - Windows OS
- For kickstart of information, please refer to the [Initial setup guide].

#Release Notes

- 2015/01/28
 - Version 0.1 Release

# How to use aremetal_ad ?

##Zabbix-Server startup

run the following file in the OS that contains the Zabbix-Server

        /usr/bin/python /usr/lib/zabbix/scheduler/caller_server.py

- The following processing is performed by the command execution
1. Get the host name of Zabbix-Server
2. Enable the state of the host
3. Import the following template file
        /usr/lib/zabbix/template/zbx_export_templates.xml
4. Create the following actions
- Mini OS automatic registration for the action
- IPMI interfaces update for the action
- Agent interfaces update for the action
- Proxy create for the action


##Mini OS initial startup

###Automatic registration process

- Attach SSH Agent Templates


###Automatic execution from SSH Agent

- Insert IPMI IP Address to the [Key:ssh.run[dcmi]] of SSH Agent

###When the value is registered in the Key of SSH Agent


- Run the following in the trigger


    /usr/bin/python /usr/lib/zabbix/scheduler/caller_action.py "UpdateIpmiInterfaces" "{HOST.NAME}"

- The following processing is performed by the command execution
1. Get IPMI IP Address from the SSH Agent of key
2. Register the IPMI IP Address to IPMI Interface to host
3. Change IPMI connection set to any setting
4. Attach host group
5. Get product name than ipmitool command
6. Attach each template (including the Trapper template) by product_name
7. Call the Schedule, Get Proxy name
8. If the Proxy to assign exists, rewrites the value of zabbix_agentd.conf
9. Remove SSH Agent template
10. Remove Agent Interface


##Actual OS initial startup

###Run the following command

    /usr/bin/python /usr/lib/zabbix/scheduler/client_startup/zabbix_client_startup.py <server ipaddress> <zabbix server username> <zabbix server password> <host name> <client ipaddress>

- Insert client ipaddress to the [Key:agent_ip] of Trapper

If boot OS is for a Proxy

- Insert hostname to the [Key:proxy.name] of Trapper


###When it is registered a value to the Trapper of [Key:agent_ip]

Run the following in the trigger

    /usr/bin/python /usr/lib/zabbix/scheduler/caller_action.py "UpdateAgentInterfaces" "{HOST.NAME}"


1. Get ipaddress from the trigger of key
2. Register the address to the agent interface of the host
3. Attach template for the agent interface


###When it is registered a value to the Trapper of [Key:proxy.name]


    /usr/bin/python /usr/lib/zabbix/scheduler/caller_action.py "CreateProxy" "{HOST.NAME}"

1. Get ProxyName from the trigger of key
2. Creating a proxy



# Contact

Please send feedback to us.

[TIS Inc.](http://www.tis.co.jp)
Strategic Technology Center  
<tech-sketch@pj.tis.co.jp>.


#License

Baremetal AutoDiscovery Tool for Zabbix is released under the Apache License version2.0. The Apache License version2.0 official full text is published at this
[link](http://www.apache.org/licenses/LICENSE-2.0.html).

Copyright 2015 TIS Inc.
