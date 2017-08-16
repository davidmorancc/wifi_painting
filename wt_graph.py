#!/usr/bin/env python
#########################################################################################
#	wt_graph																			#
#  	This utility runs the airport utility included on OSX and parses the output to		#
#	include mac, ssid, and rssi															#
#########################################################################################

#sets the about of random 'shake' in the drawing
shake_amount 		= 44
#sets the bg color
background_color 	= 'white'
#default color table
color_table = 'orange'

color_table_orange = ['#e8b999','#e9a87b','#ea9960','#e88846','#e87424','#e76b15']


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
		if opt in ("-h", "--help"):
			print 'wt_graph.py --route=<routeid>[,<routeid2>,...]'
			sys.exit()
		elif opt in ("-r", "--route"):
			route = arg	
		elif opt in ("-c", "--color"):
			color_table = arg	

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

#gets the color for the specified strength based on the color_table specified in the options or arguments
def get_colortable(color_number):
	
	
	return color_table_orange[color_number]

def get_line_color(rssi):
	rssi = abs(mean(rssi))
	
	if rssi <= 50:
		line_color = get_colortable(0)
	elif rssi <= 60:
		line_color = get_colortable(1)
	elif rssi <= 70:
		line_color = get_colortable(2)
	elif rssi <= 80:
		line_color = get_colortable(3)
	elif rssi <= 90:
		line_color = get_colortable(4)
	elif rssi <= 100:
		line_color = get_colortable(5)
		
	return line_color
	
def get_line_width(rssi):
	rssi = abs(mean(rssi))
	
	if rssi <= 50:
		line_width = .55
	elif rssi <= 60:
		line_width = .50
	elif rssi <= 70:
		line_width = .45
	elif rssi <= 80:
		line_width = .30
	elif rssi <= 90:
		line_width = .25
	elif rssi <= 100:
		line_width = .20
		
	return line_width

if __name__ == "__main__":
	#parse the arguments
	parse_arg(sys.argv[1:])

	fig = plt.figure(facecolor = background_color)
	ax = plt.Axes(fig, [0., 0., 1., 1.], )
	ax.set_aspect('equal')
	ax.set_axis_off()
	fig.add_axes(ax)
	


	#get a list of all seen macs
	for mac in database_get_macs(route):

		#get two random numbers to 'shake' the plot line
		shake = random.randrange(1,shake_amount) * .0001
		shake2 = random.randrange(1,shake_amount) * .0001
	
		#get all the log entries for a single mac
		for line in database_search_mac(mac[0],mac[1]):
			lat.append(float(line[4])+shake)
			lon.append(float(line[5])+shake2)
			rssi.append(int(line[3]))
			
		#take the lat and long lists and plot them
		plt.plot(lon, lat, color = get_line_color(rssi), lw = get_line_width(rssi), alpha = 0.5)
		print "PLOTTING - MAC Address:",str(mac[0]),"Route:",str(mac[1])

		lat = []
		lon = []
		rssi = []

	print "Total MACs seen:",len(database_get_macs(route)),"\tRoute set to:",route

	#create the graph and save
	timestamp = int(time.time())
	filename = 'output/wifi_tracks_' + str(timestamp) +'.png'
	plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=3000)

	#opens the file we just created in the os default program
	print "Opening File..."
	os.system("open "+filename)

