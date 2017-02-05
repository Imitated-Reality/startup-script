from wifi import Cell, Scheme
import os.path
import subprocess
import json
import time

conf_flag = os.path.exists('/var/www/html/config.json')
conf_dhcp = os.path.exists('/etc/dhcp/dhcpd.conf')
if not conf_dhcp:
	subprocess.check_output(['sudo', 'touch', '/etc/dhcp/dhcpd.conf'])

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

def StartHotspot():
	try:
		subprocess.check_output(['sudo', 'mv', '/etc/dhcp/dhcpd.conf', '/etc/dhcp/o-dhcpd.conf'])
		subprocess.check_output(['sudo', 'cp', 'dhcpd.conf', '/etc/dhcp/dhcpd.conf'])
		subprocess.check_output(['sudo', 'rfkill', 'unblock', 'wlan'])
		subprocess.check_output(['sudo', 'ifconfig', 'wlan0', '10.0.0.1/24', 'up'])
		subprocess.check_output(['sudo', 'service', 'isc-dhcp-server', 'restart'])
		p = subprocess.check_output(['sudo', 'hostapd', '-B', 'hostapd.conf'])
	except Exception as e:
		print str(e)	
			
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
	print "Starting Hotspot"
	StartHotspot()
