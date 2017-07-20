"""dynip 0.1a
Copyright (c) 2016-2017, Jordan Dunn.

Usage:
  dynip.py  [-h | --help]
  dynip.py  [-v | --version]
  dynip.py  [-d | --debug]
  dynip.py  [--print-zones]
  dynip.py  [--print-subzones ZONE]

Options:
  -h  --help  Display this message
  -v  --version  Display the current version number
  -d  --debug  Enables the debug parameter for the cloudflare object
  --print-zones  Prints all zones attached to the account provided
  --print-subzones ZONE  Prints all subzones for the zone provided

"""

import requests
import CloudFlare
import time
import json, pprint
from docopt import docopt


def update(client, zone, subzone, name, ip):
    '''This function updates the ip address'''
    try:
        data = {'type': 'A', 'name': name, 'content': ip}
        res = client.zones.dns_records.put(zone, subzone, data=data)
        print('✓')
    except CloudFlare.exceptions.CloudFlareAPIError as err:
        print('✗')
        print('⚠  Could not update IP address: {0}'.format(err))


def read_config(filename):
    '''Reads the configuration file to get the zones and subzones to be updated'''
    try:
        data = ""
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except IOError as err:
        print('⚠  Could not read configuration file: {0}'.format(err))


def print_zones(client):
    '''Prints the zone ids for all zones tied to the account'''
    try:
        print("Printing zones")
        zones = client.zones.get()
        for zone in zones:
            print("{0}  {1}".format(zone['name'], zone['id']))
    except CloudFlare.exceptions.CloudFlareAPIError as err:
        print('⚠  Could not get zone info: {0}'.format(err))


def print_subzones(client, zone):
    '''Prints all subzones for a given zone'''
    try:
        print("Printing subzones for zone id {0}".format(zone))
        subzones = client.zones.dns_records.get(zone)
        for subzone in subzones:
            print('{0}  {1}'.format(subzone['name'], subzone['id']))
    except CloudFlare.exceptions.CloudFlareAPIError as err:
        print('⚠  Could not get subzone info: {0}'.format(err))


if __name__ == '__main__':
    CONFIG_FILENAME = 'zones.json'
    IP = ''
    SLEEP = 60

    arguments = docopt(__doc__, version="dynip 0.1a")
    # print(arguments)

    if arguments['-v'] or arguments['--version']:
        print("dynip 0.1a")
        exit()

    if arguments['-d'] or arguments['--debug']:
        client = CloudFlare.CloudFlare(debug=True)
    else:
        client = CloudFlare.CloudFlare(debug=False)

    if arguments['--print-zones']:
        print_zones(client)
        exit()
    elif arguments['--print-subzones']:
        zone = arguments['--print-subzones']
        print_subzones(client, zone)
        exit()

    zones = read_config(CONFIG_FILENAME)

    while True:
        try:
            current_ip = requests.get('https://api.ipify.org').text
        except requests.exceptions.ConnectionError as err:
            current_ip = IP
            print('⚠  There is a problem with the connection, retrying in {0} seconds'.format(SLEEP))
        if current_ip != IP:
            print('ℹ  Detected a change in IP address. Updating records.')
            for zone in zones.values():
                print('{0}: {1}'.format(zone['name'], zone['id']))
                for subzone in zone['subzones']:
                    print('➥ {0}: {1} '.format(subzone['name'], subzone['id']), end='')
                    update(client, zone['id'], subzone['id'], subzone['name'], current_ip)
            IP = current_ip
        time.sleep(SLEEP)
