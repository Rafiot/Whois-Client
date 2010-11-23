#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script initializing the redis database of assignations, used by the sorting processes. 
It defines also the options of the differents servers. 
"""

config_file = "/mnt/data/ISFATES-DFHI/Masterarbeit/repos/WhoisClient/etc/whois_client.conf"


import re
import IPy

# 'address' : option(s)
whois_pre_options = {
    #'whois.ripe.net' :  '-B ', 
    'riswhois.ripe.net' : '-M '
    }

whois_keepalive_options = {
    'whois.ripe.net' : '-k ', 
    'riswhois.ripe.net' : '-k '
    }
    
whois_post_options = {
    'whois.nic.ad.jp' : ' /e '
    }

whois_port_options = {}

assign_table = {}
set_urls = set()
url_options = {}

def parse(assignations):
    for ip,url in assignations:
        if url not in ['UNALLOCATED', '6to4', 'teredo', '6bone', 'v6nic']:
            if not re.findall('\.',url):
                url = 'whois.' + url + '.net'
        # All the urls has to be pushed in the list: 
        # elsewhere there is no running process to put them out of redis...
        set_urls.add(url)
        # Buggy networks
        if ip == '210.71.128.0/16':
            ip = '210.71.128.0/17'
        if ip == '210.241.0.0/15':
            ip = '210.241.0.0/16'
        if ip == '221.138.0.0/13':
            ip = '221.138.0.0/15'
        net = IPy.IP(ip)
        assign_table[str(net)] = url

def set_options():
    for url in set_urls:
        url_options[url] = ['', '', '', '']
        
        pre = whois_pre_options.get(url,  '')
        post = whois_post_options.get(url,  '')
        keepalive = whois_keepalive_options.get(url,  '')
        port = whois_port_options.get(url,  43)
        if pre:
            url_options[url][0] = pre
        if post:
            url_options[url][1] = post
        if keepalive:
            url_options[url][2] = keepalive
        if port:
            url_options[url][3] = port

if __name__ == "__main__":
    import os 
    import sys
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    
    regex_ipv4 = '([^#][\d./]*)'
    regex_ipv6 = '([^#][\d\w:/]*)'
    regex_dns  = '([^#][\d\w.]*)'

    f = open('ip_del_list').read()
    assignations = re.findall('[\n]*' + regex_ipv4 + '\t' + regex_dns + '\s*',f)
    parse(assignations)

    f = open('ip6_del_list').read()
    assignations = re.findall('[\n]*' + regex_ipv6 + '\t' + regex_dns + '\s*',f)
    parse(assignations)

    # Self defined servers
    # to do the RIS Requests
    set_urls.add('riswhois.ripe.net')

    set_options()

    f = open(os.path.join(config.get('global','root'),config.get('global','assignations')), 'w')
    f.write("assignation_table = %s\nwhois_servers = %s\n" % (str(assign_table), str(url_options)))
    f.close()


