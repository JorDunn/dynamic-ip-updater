"""dynip 0.1a
Copyright (c) 2016-2017, Jordan Dunn.

Usage:
  dynip.py  (-h | --help)
  dynip.py  (-v | --version)
  dynip.py  (-z | --zones)
  dynip.py  (-sz | --subzones)

Options:
  -h  --help  Display this message
  -v  --version Display the current version number
  -z  --zones Prints out all the zones tied to the account
  -sz  --subzones Prints out all the subzones tied to the zone

"""

import requests
import CloudFlare
import time
from docopt import docopt

# you can use the .example.cfg file in this scripts dir to configure
# and rename to .cloudflare.cfg

def setup(client):
    '''This function assists the user in first time setup for zones and subzones'''
    pass

def update(client):
    '''This function updates the ip address if it detects that it has changed'''
    pass

def read_config(filename):
    '''Reads zones.json to get the zones and subzones to updated'''
    pass

if __name__ == '__main__':

    CONFIG_FILENAME = 'zones.json'
    IP = ''
    DEBUG = False
    SLEEP = 60
    client = CloudFlare.CloudFlare(debug=DEBUG)

    arguments = docopt(__doc__, version="dynip 0.1a")
    print(arguments)
    if arguments['-v'] or arguments['--version']:
        print("dynip 0.1a")
    elif arguments['-z'] or arguments['--zones']:
        pass
        # print zones
    elif arguments['-sz'] or arguments['--subzones']:
        pass
        # print subzones
