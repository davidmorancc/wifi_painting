#!/usr/bin/env python
#########################################################################################
#	wt_wordcloud																		#
#  	This utility runs the airport utility included on OSX and parses the output to		#
#	include mac, ssid, and rssi															#
#########################################################################################
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from wt_database import database_get_ssids
import sys, getopt, os
import numpy as np
import time, random

local_font_path 	= '/Library/Fonts/Arial.ttf'
background_color 	= 'black'

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

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
			
if __name__ == "__main__":
	#parse the arguments
	parse_arg(sys.argv[1:])
	
	myList = database_get_ssids(route);
	wordcloud = WordCloud(font_path=local_font_path, max_words=5000, width=4000, height=4000)
	
	words = {}
		
	for item in myList:
		new_ssid =  item[0].replace(' ', '_').replace('\'', '').replace(',', '').replace('!', '').replace('-','_').replace('.','').strip()
		new_count = item[1]
		words[new_ssid] = new_count
	
	# Display the generated image:
	# the matplotlib way:

	fig = plt.figure(facecolor = background_color)
	ax = plt.Axes(fig, [0., 0., 1., 1.], )
	ax.set_aspect('equal')
	ax.set_axis_off()
	fig.add_axes(ax)

	# lower max_font_size
	wordcloud.fit_words(words)
	plt.figure()
	plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3))
	plt.axis("off")
	
	#create the graph and save
	timestamp = int(time.time())
	filename = 'output/wifi_tracks_wordcloud_' + str(timestamp) +'.png'
	plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=4000)

	#opens the file we just created in the os default program
	print "Opening File..."
	os.system("open "+filename)