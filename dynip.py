import requests
import CloudFlare
import time

def setup(client):
    '''This function assists the user in first time setup for zones and subzones'''
    pass

if __name__ == '__main__':
    # default ip so that the script will update dns when started
    ip = '0.0.0.0'
    # fill these in with relevant data
    zone_id = ''
    subzone_id = ''
    # you can use the .example.cfg file in this scripts dir to configure
    # and rename to .cloudflare.cfg
    debug = False
    cf = CloudFlare.CloudFlare(debug=debug)
    # domain info
    type = 'A'
    name = ''

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
