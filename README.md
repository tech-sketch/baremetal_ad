Zabbix Baremetal Autodiscoverer
====

#Overview

Zabbix Baremetal Autodiscover(baremetal_ad) is an Apache2 Licensed, full baremetal monitoring tools, for OpenComputingProject(OCP) machine

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

#Release Notes

- 2015/01/28
 - Version 0.1 Release

# Install Guide

## Requirements

The following requirements exist for running this product:

- Cobbler
 - dhcpd
 - named
 - ntpd


- setp machine
 - ipmitool

## Cobbler setting

### connection from step machine to cobbler

    $ssh cobbler-server

### adding repos

1. baremetal_ad
1. MiniOS
1. CentOS6.6(x86_64)
1. CentOS6.6 updates
1. EPEL
1. Zabbix repo


#### baremetal_ad
    # mkdir -p /opt/git
    # cd /opt/git
    # git clone https://github.com/tech-sketch/baremetal_ad.git
    # cobbler repo add --name="Zabbix-OCP" --arch=src --breed=rsync --mirror=/opt/git/baremetal_ad
    # cp -rp /opt/git/baremetal_ad/kickstart_script/cobbler/kickstart/* /var/lib/cobbler/kickstart/
    # cp -rp /opt/git/baremetal_ad/kickstart_script/cobbler/snippets/* /var/lib/cobbler/snippets/

#### MiniOS (Ubuntu Server 14.04)
    # mount -o loop ubuntu-14.04-ocpinstall-amd64.iso /media/
    # cobbler import --name=OCP-MiniOS --path=/media
    # umount /media

#### CentOS6.6
    # wget http://ftp.jaist.ac.jp/pub/Linux/CentOS/6.6/isos/x86_64/CentOS-6.6-x86_64-bin-DVD1.iso
    # mount -o loop CentOS-6.6-x86_64-bin-DVD1.iso /media
    # cobbler import --name=CentOS66 --arch=x86_64 --path=/media
    # umount /media

#### CentOS6.6 updates
    # cobbler repo add --name="CentOS66x86_64mirror" --breed=yum --mirror=http://ftp.jaist.ac.jp/pub/Linux/CentOS/6.6/updates/x86_64/

#### EPEL
    # cobbler repo add --name="EPEL6" --arch=x86_64 --breed=yum --mirror=http://ftp.jaist.ac.jp/pub/Linux/Fedora/epel/6/x86_64/

#### Zabbix repo
    # cobbler repo add --name="Zabbix-for-RHEL6" --arch=x86_64 --breed=yum --mirror=http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/

### profile setting
<b>Enter the IP address of the zabbix server [[@@ZabbixServerIP@@]]</b>
    # cobbler profile edit --name="CentOS66-x86_64" --repos="zabbix-for-RHEL6-x86-64 Zabbix-OCP EPEL6-x86_64 CentOS66x86_64mirror CentOS66x86_64" --kickstart="/var/lib/cobbler/kickstart/CentOS6-x86_64.ks" --ksmeta="zabbix_server_ip=[[@@ZabbixServerIP@@]]" --kopts="console=ttyS1,115200"

    # cobbler profile edit --name="OCP-MiniOS" --kickstart="/var/lib/cobbler/kickstart/ubuntu-tis-ocp.seed" --ksmeta="zabbix_server_ip=[[@@ZabbixServerIP@@]]" --kopts="console=ttyS0 console=S4,115200"

    # cobbler profile copy --name="CentOS66-x86_64" --newname="ZabbixProxyForCentOS66-x86_64" --kickstart="/var/lib/cobbler/kickstart/ZabbixProxy-Cent6-x86_64.ks"

    # cobbler profile copy --name="CentOS66-x86_64" --newname="ZabbixServerForCentOS66-x86_64" --kickstart="/var/lib/cobbler/kickstart/ZabbixServer-Cent6-x86_64.ks" --ksmeta="zabbix_server_flg=1"

# How to use

## 1st step.

#### choice to [ZabbixServerForCentOS66-x86_64] from PXE boot menu.  
* Could you wait ...

## 2nd step.

#### Next step, choice to [OCP-MiniOS] from PXE boot menu to other server.
##### KickstartMetadata chenged "zabbix_server_ip"<br>
ex.) when zabbix-server ip is "10.0.0.101" .
    # cobbler profile edit --name="OCP-MiniOS"--ksmeta="zabbix_server_ip=10.0.0.101"

##### choice to [OCP-MiniOS] from PXE boot menu.
 * Could you wait ...

##### After completing the installation of the OS, IPMI monitoring begins.

## 3rd step.

#### Next step, choice to [CentOS6-x86_64] from PXE boot menu to other server.
##### KickstartMetadata chenged "zabbix_server_ip"<br>
ex.) when zabbix-server ip is "10.0.0.101" .
    # cobbler profile edit --name="CentOS6-x86_64"--ksmeta="zabbix_server_ip=10.0.0.101"

## How to Zabbix Proxy Server

Bare metal AD It is also possible to use a ZabbixProxy.
To use a proxy, you must have two embodiments below.
- Installation of ZabbixProxy
- Generation of Proxy allocation rules

### Installation of ZabbixProxy

#### 1.Conducted　[2nd step.] The implementation
#### 2.choice to [CentOS6-x86_64] from PXE boot menu to other server.<br>
   KickstartMetadata chenged "zabbix_server_ip"<br>

ex.) when zabbix-server ip is "10.0.0.101" .
    # cobbler profile edit --name="ZabbixProxyForCentOS66-x86_64"--ksmeta="zabbix_server_ip=10.0.0.101"

### Generation of Proxy allocation rules

#### 1.create proxy_rule.json

    # cp -rp /usr/lib/zabbix/scheduler/schedule/conf/sample_rule.json /usr/lib/zabbix/scheduler/schedule/conf/proxy_rule.json
    # vi /usr/lib/zabbix/scheduler/schedule/conf/proxy_rule.json


    {
        "ipmi_ip": {
          "[[@@proxy-name@@]]":{
            "from": "10.0.0.1",
            "to": "10.0.0.254"
          },
          "[[@@proxy-name@@]]":{
            "from": "10.0.1.1",
            "to": "10.0.1.254"
            }
          }  
    }

- rule

| Name | Function |
|------------|----------------------------------------|
| proxy-name | proxy name that is registered in the zabbix server |
| from | network range start |
| to | network range end |

<b>After you can send a comfortable ZabbixMonitoring life By carrying out the [3rd step.]

#Option Configure

<b>For each server, I am available below as kickstart metadata.

| Name | Function |　default | Supported profile |
|------------|--------------------------|--------------|------------------------------|
| zabbix_server_ip | installed master zabbix ip address | *Required | OCP-MiniOS<br>CentOS6-x86_64<br>ZabbixProxyForCentOS66-x86_64 |
| zabbix_server_flg | zabbix_agent modify skip for zabbix-server | 0 | ZabbixServerForCentOS66-x86_64 |
| zabbix_user | User name to use in api | Admin | CentOS6-x86_64<br>ZabbixServerForCentOS66-x86_64<br>ZabbixProxyForCentOS66-x86_64 |
| zabbix_password | User password to use in api | zabbix | CentOS6-x86_64<br>ZabbixServerForCentOS66-x86_64<br>ZabbixProxyForCentOS66-x86_64 |
| zabbix_agent_interface | zabbix-agent used management interface | eth0 | CentOS6-x86_64<br>ZabbixProxyForCentOS66-x86_64 |

# Contact

Please send feedback to us.

[TIS Inc.](http://www.tis.co.jp)
Strategic Technology Center  
--- for Zabbix team  
<---@ml.tis.co.jp>.


#License

Baremetal AutoDiscovery Tool for Zabbix is released under the Apache License version2.0. The Apache License version2.0 official full text is published at this
[link](http://www.apache.org/licenses/LICENSE-2.0.html).

Copyright 2015 TIS Inc.
