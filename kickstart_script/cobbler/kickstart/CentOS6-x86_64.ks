#platform=x86, AMD64, or Intel EM64T
# System authorization information
auth  --useshadow  --enablemd5
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all --initlabel
# Use text mode install
text
# Firewall configuration
firewall --disabled
# Run the Setup Agent on first boot
firstboot --disable
# System keyboard
keyboard jp106
# System language
lang en_US
# Use network installation
url --url=$tree
# If any cobbler repo definitions were referenced in the kickstart profile, include them here.
$yum_repo_stanza
# Network information
$SNIPPET('network_config')
# Reboot after installation
reboot

#Root password
rootpw --iscrypted $default_password_crypted
# SELinux configuration
selinux --disabled
# Do not configure the X Window System
skipx
# System timezone
timezone  Asia/Tokyo
# Install OS instead of upgrade
install
# Clear the Master Boot Record
zerombr
# Allow anaconda to partition the system as needed
autopart

%packages

@base
@core
@japanese-support
@development
@legacy-unix

%pre

$SNIPPET('log_ks_pre')

wget "http://$server:$http_port/cblr/svc/op/yum/profile/CentOS6-x86_64" -O /dev/null

%post --log=/root/ks-post.log

wget "http://$server:$http_port/cblr/svc/op/yum/profile/CentOS6-x86_64" --output-document=/etc/yum.repos.d/cobbler-config.repo

# ZabbixServer ZabbixAgent Install
# Kickstart Metadata get

$SNIPPET('pre_install_zabbix_agent')

# Start koan environment setup
$SNIPPET('koan_environment')

# Zabbix Tune wait
/bin/sleep 300

%end
