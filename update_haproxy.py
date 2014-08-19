""""
This is a quick hack to update haproxy with marathon ip:port

"""
import os
import requests

MARATHON_URL = "http://10.0.0.68:8080/"
APP = '3333'

HAPROXY_CONFIG_FILE = """
global
	log /dev/log	local0
	log /dev/log	local1 notice
	chroot /var/lib/haproxy
	user haproxy
	group haproxy
	daemon
	stats socket    /tmp/haproxy

defaults
	log	global
	mode	http
	option	httplog
	option	dontlognull
        contimeout 5000
        clitimeout 50000
        srvtimeout 50000
	errorfile 400 /etc/haproxy/errors/400.http
	errorfile 403 /etc/haproxy/errors/403.http
	errorfile 408 /etc/haproxy/errors/408.http
	errorfile 500 /etc/haproxy/errors/500.http
	errorfile 502 /etc/haproxy/errors/502.http
	errorfile 503 /etc/haproxy/errors/503.http
	errorfile 504 /etc/haproxy/errors/504.http

listen mesos 0.0.0.0:5000
	mode	http
	stats uri /haproxy
"""


def get_mesos_app_hosts_list():
    r = requests.get(MARATHON_URL + "v2/apps/" + APP)
    body = r.json()
    if 'app' not in body:
        return ""
    haproxy_host_line = ""
    for container in body['app']['tasks']:
        haproxy_host_line += ("\tserver %s %s:%s check\n" % (
                              container['id'], container['host'],
                              container['ports'][0]))
    return haproxy_host_line


if __name__ == '__main__':
    app_hosts = get_mesos_app_hosts_list()
    with open("/etc/haproxy/haproxy.cfg", "w") as f:
        f.write(HAPROXY_CONFIG_FILE)
        f.write(app_hosts)
    os.system("/etc/init.d/haproxy restart")
