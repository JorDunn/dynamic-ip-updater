import requests
import CloudFlare
import time

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

    # Most of the stuff below is going to be discarded
    while True:
        if zone_id == '':
            print("Printing zone id for all domains")
            res = cf.zones.get()
            for zone in res:
                print(zone['name'], "=", zone['id'])
            print("Please configure this script with the domain id and run again for subdomain ids")
            exit()
        elif subzone_id == '':
            print("Printing zone id for all subdomains")
            res = cf.zones.dns_records.get(zone_id)
            for subzone in res:
                print(subzone['name'], "=", subzone['id'])
            print("Please configure this script with the subdomain id")
            exit()
        else:
            res = requests.get("https://api.ipify.org").text
            if ip != res:
                print("Old external IP: ", ip)
                print("New external IP: ", res)
                ip = res
                data = {'type': type, 'name': name, 'content': ip}
                print(data)
                try:
                    print(data)
                    res = cf.zones.dns_records.put(zone_id, subzone_id, data=data)
                    print(res)
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    if len(e) > 0:
                        for err in e:
                            print("Error:", err)
                        exit()
        time.sleep(60)
