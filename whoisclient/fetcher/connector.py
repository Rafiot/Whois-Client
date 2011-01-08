#!/usr/bin/python
# -*- coding: utf-8 -*-

config_file = "../etc/whois_client.conf"

import ConfigParser
import os
config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), config_file))
use_syslog = config.get('global','use_syslog')

if use_syslog:
    import syslog
    syslog.openlog('Whois_Connector', syslog.LOG_PID, syslog.LOG_USER)
    
from assignations import *
import IPy

def get_server(query):
    query = IPy.IP(query)
    to_return = IPy.IP('0.0.0.0/0')
    for subnet in assignation_table:
        subnet = IPy.IP(subnet)
        if subnet in to_return:
            if query in subnet:
                to_return = subnet
    return assignation_table[str(to_return)]

from whois_fetcher import *

class Connector(object):
    """
    Make queries to a specific Whois server
    """
    support_keepalive = config.get('servers', 'support_keepalive').split()
    
    def __init__(self, queries, server = None, keepalive = False):
        """
        Initialize the two connectors to the redis server, set variables depending on the server
        Initialize a whois fetcher on this server
        """
        if type(queries) is not type([]):
            queries = [queries]

        self.server = server
        if self.server is None:
            self.queries = self.sort_queries(queries)
        else:
            self.queries = {server: queries}

        self.keepalive = keepalive
        
    
    def sort_queries(self, queries):
        to_return = {}
        for query in queries:
            server = get_server(query)
            list_by_server = to_return.get(server, None)
            if list_by_server is None:
                to_return[server] = [query]
            else:
                to_return[server].append(query)
        return to_return
        
    def fetch(self):
        self.responses = {}
        for server, queries in self.queries.iteritems():
            if len(queries) > 1 and server in support_keepalive:
                self.keepalive = True
            try:
                f = WhoisFetcher(server)
                for query in queries:
                    self.responses[query] = [server, f.fetch_whois(query, self.keepalive)]
            except IOError as text:
                error_msg = "IOError on " + self.server + ': ' + str(text)
                if use_syslog:
                    syslog.syslog(error_msg)
                else:
                    print(error_msg)                
        return self.responses

if __name__ == "__main__":
    c = Connector('127.0.0.1')
    print c.fetch()