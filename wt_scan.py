#!/usr/bin/env python
#########################################################################################
#	wt_scan																				#
#  	This utility runs the airport utility included on OSX and parses the output to		#
#	include mac, ssid, and rssi															#
#########################################################################################

import subprocess
import re
import time

AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

#getWifi function
#returns mac_address, ssid, and rssi from the airport utility on mac osx
def getWifi():
	mac_address = ""
	ssid = ""
	rssi = ""
	return_wifi = []

	#run the airport utility with the scan option
	process = subprocess.Popen([AIRPORT_PATH, "--scan"], stdout=subprocess.PIPE)
	#pipe the output to a string
	out, err = process.communicate()
	#airport likes a 1 sec delay between runs otherwise it misses, 
	#time.sleep(1) #fixed this by running as su

	for line in out.splitlines():

		#search the line for the mac address
		#do this error handler since some lines wont have mac/ssid info
		try:
			mac_address = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', line, re.I).group().strip()
			mac_address = re.sub('[:]', '', mac_address)		#remove the : from the mac addresses
			ssid = re.search(r'(?:(?!([0-9A-F]{2}[:-]){5}([0-9A-F]{2})).)*', line, re.I).group().strip()
			rssi = re.search(r'(?<=([0-9A-F]{2}[:-]){5}([0-9A-F]{2}))[^\]]{4}', line, re.I).group().strip()
		
			return_wifi.append([mac_address, ssid, rssi])
		except:
			pass
			
	return return_wifi

#if run directly output the wifi scan
if __name__ == "__main__":
	
	for line in getWifi():
		print "Mac Address: %s\t\tRSSI: %s\t\tSSID: %s" % (line[0], line[2], line[1])

	
	
