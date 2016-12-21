from wifi import Cell, Scheme
import os.path
import json

file_path = '/var/www/html/config.json'
conf_flag = os.path.exists(file_path)

def ConnectNetwork(ssid, psk):
	for cell in Cell.all('wlan0'):
	        if cell.ssid == ssid:
	                scheme = Scheme.find('wlan0', 'local')
	                if scheme==None:
	                        scheme = Scheme.for_cell('wlan0', 'local', cell, psk)
	                        scheme.save()
	                
			try:
				scheme.activate()
				return 0
			except:
				return 1
			
if conf_flag:
	data = open(file_path, 'r')
	json_data = json.load(data)
	#print(json_data['username'] + " " + json_data['password'] + " " + json_data['ssid'] + " " + json_data['passkey'])
	status = ConnectNetwork(json_data['ssid'], json_data['passkey'])
	if status == 0:
		print "Connected to Local Network"
	else:
		print "Unable to connect to network"

else:
	print "Call Script to Start Hotspot"
