import requests, CloudFlare, time

if __name__ == '__main__':
	ip = '0.0.0.0'
	print("External IP: " + ip)
	cf = CloudFlare.CloudFlare()
	
	while(True):
		res = requests.get("https://api.ipify.org").text
		if ip != res:
			print("New external IP: " + res)
			ip = res
		try:
			
		time.sleep(60)
