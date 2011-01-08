#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os

setup(
    name='WhoisClient',
    version='1.0dev',
    author='Raphaël Vinot',
    author_email='raphael.vinot@gmail.com',
    packages=['whoisclient', 'whoisclient.fetcher', 'whoisclient.whois_parsers'],
    scripts=['bin/pyRIS','bin/pywhois'],
    url='http://gitorious.org/python-whois',
    platforms = ['Linux'],
    license='LICENSE.txt',
    description='A small (RIS) Whois client.',
    long_description=open('README.txt').read(),
    package_data={'whoisclient' : ['etc/whois_client.conf']}
)
