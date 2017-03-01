#!/usr/bin/env python
#########################################################################################
#	wifiRoutes																			#
#  	This utility runs the airport utility included on OSX and parses the output to		#
#	include mac, ssid, and rssi															#
#########################################################################################

import SocketServer
from wt_scan import getWifi
from wt_gps_nmea import convert_gpgga
from wt_database import database_insert
from wt_database import database_close
from wt_database import database_commit
import datetime
print datetime.datetime.utcnow().isoformat()
HOST, PORT = "172.20.10.2", 11121

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
    	count = 0
    	while 1:
			# self.request is the TCP socket connected to the client
			try:
				self.data = self.request.recv(1024).strip()
				
				count += 1
				if count > 2000000:
					break
				if self.data:
					count = 0
					gps_data = convert_gpgga(self.data)
					
					print "GPS Data Recived from %s: Lat:%s Long:%s Alt:%s" % (self.client_address[0],str(gps_data[0]),str(gps_data[1]),str(gps_data[2]))
					
					for wifi_network in getWifi():
						#get the date in 8601 format for the gpx file
						date_iso8601 = datetime.datetime.utcnow().isoformat()
						
						#insert into the database
						database_insert(wifi_network[0],wifi_network[1],wifi_network[2],str(gps_data[0]),str(gps_data[1]),str(gps_data[2]),str(date_iso8601))
						
						#print a line
						print "Time: %s Lat: %s Long: %s Alt: %s Mac: %s RSSI: %s SSID: %s" % (date_iso8601,str(gps_data[0]),str(gps_data[1]),str(gps_data[2]),wifi_network[0],wifi_network[2],wifi_network[1])

					database_commit()
			except KeyboardInterrupt:
				print "Closing server..."
				break


if __name__ == "__main__":

    # Create the server, binding to localhost on port 9999
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print "Closing server..."
    server.server_close()
    database_close()
    quit()
    