#!/usr/bin/env python
#########################################################################################
#	wt_graph																			#
#  	This utility runs the airport utility included on OSX and parses the output to		#
#	include mac, ssid, and rssi															#
#########################################################################################

import matplotlib.pyplot as plt
from wt_database import database_get_macs
from wt_database import database_search_mac
import os
import time
import random, sys,  getopt

lat 	= []
lon 	= []
rssi 	= []

shake 	= 0
shake2	= 0
route 	= ''

#parse out our command line arguments
def parse_arg(argv):
	global route
	route = '%'
	try:
		opts, args = getopt.getopt(argv,"h:r",["help","route="])
	except getopt.GetoptError:
		print 'wt_graph.py --route=<routeid>[,<routeid2>,...]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'wt_graph.py --route=<routeid>[,<routeid2>,...]'
			sys.exit()
		elif opt in ("-r", "--route"):
			route = arg	

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
    
def get_line_color(rssi):
	rssi = abs(mean(rssi))
	
	if rssi <= 50:
		line_color = 'orangered'
	elif rssi <= 60:
		line_color = 'chocolate'
	elif rssi <= 70:
		line_color = 'yellow'
	elif rssi <= 80:
		line_color = 'orange'
	elif rssi <= 90:
		line_color = 'darkorange'
	elif rssi <= 100:
		line_color = 'coral'
		
	return line_color
	
def get_line_width(rssi):
	rssi = abs(mean(rssi))
	
	if rssi <= 50:
		line_width = .20
	elif rssi <= 60:
		line_width = .25
	elif rssi <= 70:
		line_width = .30
	elif rssi <= 80:
		line_width = .40
	elif rssi <= 90:
		line_width = .45
	elif rssi <= 100:
		line_width = .50
		
	return line_width

if __name__ == "__main__":
	#parse the arguments
	parse_arg(sys.argv[1:])

	fig = plt.figure(facecolor = '0.05')
	ax = plt.Axes(fig, [0., 0., 1., 1.], )
	ax.set_aspect('equal')
	ax.set_axis_off()
	fig.add_axes(ax)

	#get a list of all seen macs
	for mac in database_get_macs(route):

		#get two random numbers to 'shake' the plot line
		shake = random.randrange(1,33) * .0001
		shake2 = random.randrange(1,33) * .0001
	
		#get all the log entries for a single mac
		for line in database_search_mac(mac[0],route):
			lat.append(float(line[4])+shake)
			lon.append(float(line[5])+shake2)
			rssi.append(int(line[3]))
			
		#take the lat and long lists and plot them
		plt.plot(lon, lat, color = get_line_color(rssi), lw = get_line_width(rssi), alpha = 0.5)
		print "Plotting data for MAC Address:",str(mac[0])

		lat = []
		lon = []
		rssi = []

	print "Total MACs seen:",len(database_get_macs(route)),"\tRoute set to:",route

	#create the graph and save
	timestamp = int(time.time())
	filename = 'output/wifi_routes_' + str(timestamp) +'.png'
	plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=300)

	#opens the file we just created in the os default program
	print "Opening File..."
	os.system("open "+filename)

