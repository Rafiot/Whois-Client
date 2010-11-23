#!/usr/bin/python
# -*- coding: utf-8 -*-

from fetcher.connector import * 
from whois_parsers.whois_parsers import * 

class WhoisClient(object):
    
    def __init__(self, server = None, keepalive = False):
        self.use_server(server)
        self.set_keepalive(keepalive)
        self.parsed_responses = []

    def simple_queries(self, queries):
        c = Connector(queries, self.server, self.keepalive)
        self.responses = c.fetch()
        
    def parse_queries(self, queries):
        self.simple_queries(queries)
        for query, infos in self.response.iteritems():
            self.parsed_responses.append(WhoisParsers(infos[1], infos[0]))
 
    def ris_queries(self, queries):
        c = Connector(queries, "riswhois.ripe.net")
        self.response = c.fetch()
        for query, infos in self.response.iteritems():
            self.parsed_responses.append(WhoisParsers(infos[1], infos[0]))
    
    def use_server(self, server):
        self.server = server

    def set_keepalive(self, keepalive):
        self.keepalive = keepalive
