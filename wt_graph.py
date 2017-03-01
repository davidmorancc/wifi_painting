#!/usr/bin/env python
#########################################################################################
#	wr_graph																			#
#  	This utility runs the airport utility included on OSX and parses the output to		#
#	include mac, ssid, and rssi															#
#########################################################################################

import matplotlib.pyplot as plt
from wt_database import database_get_macs
from wt_database import database_search_mac
import os
import time

lat = []
lon = []

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

#get a list of all seen macs
for mac in database_get_macs():
	
	#get all the log entries for a single mac
	for line in database_search_mac(mac[0]):
		lat.append(line[3])
		lon.append(line[4])
		
	#take the lat and long lists and plot them
	print "Plotting data for MAC Address:",str(mac[0])
	plt.plot(lon, lat, color = 'deepskyblue', lw = 0.2, alpha = 0.8)
	
	lat = []
	lon = []

print "Total MACs seen:",len(database_get_macs())

#create the graph and save
timestamp = int(time.time())
filename = 'output/wifi_routes_' + str(timestamp) +'.png'
plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=300)

#opens the file we just created in the os default program
print "Opening File..."
os.system("open "+filename)