#!/usr/bin/python
# -*- coding: utf-8 -*-

config_file = "/mnt/data/ISFATES-DFHI/Masterarbeit/repos/WhoisClient/etc/whois_client.conf"

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read(config_file)
sleep_timer = int(config.get('global','short_timer'))
use_syslog = config.get('global','use_syslog')

from socket import *
import time

from assignations import *

if use_syslog:
    import syslog
    syslog.openlog('BGP_Ranking_Fetchers', syslog.LOG_PID, syslog.LOG_USER)

class WhoisFetcher(object):
    """Class to fetch the Whois entry of a particular IP.
    """
    
    def connect(self):
        """
        TCP connection to one on the whois servers
        """
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((self.server,self.port))
        self.connected = True
        
        
    def disconnect(self):
        """
        Close the TCP connection 
        """
        self.s.close()
        self.connected = False
    
    def fetch_whois(self, query, keepalive = False):
        """
        Fetch the whois informations. Keep the connection alive if needed. 
        """
        if not self.connected:
            self.connect()
        if keepalive:
            self.pre_options += self.keepalive_options
        self.s.send(self.pre_options + query + self.post_options +' \n')
        self.text = ''
        loop = 0
        fs = self.s.makefile()
        prec = ''
        while 1:
            temp = fs.readline()
            if not temp or len(temp) == 0 or prec == temp == '\n':
                break
            self.text += temp 
            prec = temp 
        if len(self.text) == 0:
            error_msg = "error (no response) with query: " + query + " on server " + self.server
            if use_syslog:
                syslog.syslog(syslog.LOG_ERR, error_msg)
            else:
                print(error_msg)
            time.sleep(sleep_timer)
        if not keepalive:
            self.disconnect()
        return self.text

    def __set_values(self,  server):
        """
        Set the needed informations concerning the server we want to use
        """
        self.server = server
        options = whois_servers[server]
        self.pre_options = options[0]
        self.post_options = options[1] 
        self.keepalive_options = options[2]
        self.port = options[3]

    def __init__(self, server):
        self.__set_values(server)
        self.connected = False
    
    def __repr__(self):
        return self.text

if __name__ == "__main__":
    f = WhoisFetcher('whois.arin.net')
    print(f.fetch_whois('127.0.0.1', False))
    print(f.fetch_whois('127.0.0.1', False))
    print(f.fetch_whois('127.0.0.1', False))
    f = WhoisFetcher('whois.ripe.net')
    print(f.fetch_whois('127.0.0.1', True))
    print(f.fetch_whois('127.0.0.1', True))
    print(f.fetch_whois('127.0.0.1', False))
    f = WhoisFetcher('whois.lacnic.net')
    print(f.fetch_whois('200.3.14.10', False))
    
    f = WhoisFetcher('whois.apnic.net')
    print(f.fetch_whois('116.66.203.208', False))
    
    f = WhoisFetcher('riswhois.ripe.net')
    print(f.fetch_whois('200.3.14.10', False))
  
    
    
