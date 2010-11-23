#!/bin/bash

# This script write ${CONFIG_PATH} in every files where ${VARIABLE} is found.
# Like this it is possible to modify on a simple way the path to the config file for every files using it. 
# The other advantage of this method is that all the python files knows the absolute path to the config file,
# each of them is usable from everywhere.


ROOT_PROJECT="/mnt/data/ISFATES-DFHI/Masterarbeit/repos/WhoisClient"
VARIABLE="config_file ="
CONFIG_PATH="\/mnt\/data\/ISFATES-DFHI\/Masterarbeit\/repos\/WhoisClient\/etc\/whois_client.conf"

echo "find ${ROOT_PROJECT} -name \"*.py\" -exec sed -i 's/\(${VARIABLE}\).*/\1${CONFIG_PATH}/' {} \;"

find ${ROOT_PROJECT} -name "*.py" -exec sed -i 's/^\('"${VARIABLE}"'\).*$/\1 "'"${CONFIG_PATH}"'"/' {} \;

