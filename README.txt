============
Whois Client
============

Whois client fully written in Python. It uses the list of assignations provided
by the whois client of debian (https://github.com/weppos/whois-debian).

History
===========
To parse the whois entries, it uses an improved version of pywhois:
https://code.google.com/p/pywhois/
but the basic idea is the same. 

Usage
==========
To get a whois entry:
    pywhois <IP>

To get a RIS entry: 
    pyRIS <IP>

More information on how to use the lib ASAP.


Why
===========
This code has been first written to be used in bgp ranking:
http://gitorious.org/bgp-ranking
but it is now a standalone project.
