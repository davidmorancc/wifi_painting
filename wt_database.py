#!/usr/bin/env python
#########################################################################################
#	wt_database																			#
#  	This utility is to handle the database setup and read/writing						#
#	Accepts the command line arguments 'create' and 'empty' to handle setting up a new  #
#	database if the file gets delete and clearing out the database after exporting data #
#########################################################################################

import sqlite3
import sys

connection = sqlite3.connect('db/log.db')
database = connection.cursor()

#function to create a new database and setup the tables
def database_create():	
	#create our table
	database.execute('''CREATE TABLE `log` (
	`route`	TEXT,
	`mac`	TEXT,
	`ssid`	TEXT,
	`rssi`	TEXT,
	`lat`	TEXT,
	`long`	TEXT,
	`alt`	TEXT,
	`time`	TEXT
	);''')
	
	#go ahead commit the database
	connection.commit()
	
	print "Created new database and commited"
	
	return

#function to empty the database
def database_empty():
	database.execute("DELETE FROM log")
	database.execute("VACUUM")
	connection.commit()
	
	print "Cleared database and commited"
	return

#route, mac, ssid, rssi, timestamp, lat, long, alt
def database_insert(route, mac,ssid,rssi,lat,long,alt,time):
	database.execute("INSERT INTO log (route, mac,ssid,rssi,lat,long,alt,time) VALUES (?,?,?,?,?,?,?,?)", (route, mac, ssid, rssi, lat, long, alt, time))
	return
	
#commit and close the database	
def database_close():	
	connection.commit()
	connection.close()
	return
	
#commit and close the database	
def database_commit():	
	connection.commit()
	return 
	
#returns a list of all the entries for the given mac address
def database_search_mac(mac, route):
	database.execute("SELECT route,mac,ssid,rssi,lat,long,alt,time FROM log WHERE mac = ? AND route LIKE ?",(mac,route,))
	rows = database.fetchall()
	return rows

#returns a list of all mac addresses found	
def database_get_macs(route):	
	rows = []
	for line in route.split(","):
		database.execute("SELECT DISTINCT mac, '"+line+"' FROM log WHERE route LIKE ?", (line,))
		rows = rows + database.fetchall()
	return rows

def database_get_ssid():	
	database.execute("SELECT count (DISTINCT ssid) FROM log")
	return (database.fetchall()[0][0])

#prints a list of all routes found	
def database_get_routes():	
	database.execute("SELECT DISTINCT route FROM log")
	for route in database.fetchall():
		print route[0]
	return 
	
#returns a list of all ssids found for the route given
def database_get_ssids(route):	
	rows = []
	for line in route.split(","):
		database.execute("SELECT ssid, count(ssid) FROM log WHERE route LIKE ? GROUP BY ssid", (line,))
		rows = rows + database.fetchall()
	return rows

if __name__ == "__main__":
	
	#setup the command line arguments create and empty
	for arg in sys.argv:
		if arg == "create":
			database_create()
		if arg == "empty":
			database_empty()
		if arg == "routes":
			database_get_routes()
		if arg == "ssids":
			print "Total SSIDs:", database_get_ssid()
	database_close()


