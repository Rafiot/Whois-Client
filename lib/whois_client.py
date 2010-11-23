#!/usr/bin/python
# -*- coding: utf-8 -*-

from fetcher.connector import * 
from parser.whois_parsers import * 

class WhoisClient(object):
    
    def __init__(self, server = None, keepalive = False):
        self.use_server(server)
        self.set_keepalive(keepalive)

    def simple_queries(self, queries):
        print queries
        c = Connector(queries, self.server, self.keepalive)
        self.response = c.fetch()
        self.parsed_responses = []
        for query, infos in self.response.iteritems():
            self.parsed_responses.append(WhoisParsers(infos[1], infos[0]))
    
    def use_server(self, server):
        self.server = server

    def set_keepalive(self, keepalive):
        self.keepalive = keepalive
    
    def do_query(self, objects):
        pass