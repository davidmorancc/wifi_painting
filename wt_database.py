#!/usr/bin/env python
#########################################################################################
#	wr_database																			#
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
	
	return

#function to empty the database
def database_empty():
	database.execute("DELETE FROM log")
	database.execute("VACUUM")
	connection.commit()
	return

#mac, ssid, rssi, timestamp, lat, long, alt
def database_insert(mac,ssid,rssi,lat,long,alt,time):
	database.execute("INSERT INTO log (mac,ssid,rssi,lat,long,alt,time) VALUES (?,?,?,?,?,?,?)", (mac, ssid, rssi, lat, long, alt, time))
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
def database_search_mac(mac):	
	database.execute("SELECT mac,ssid,rssi,lat,long,alt,time FROM log WHERE mac = '" + mac + "'")
	rows = database.fetchall()
	return rows

#returns a list of all mac addresses found	
def database_get_macs():	
	database.execute("SELECT DISTINCT mac FROM log")
	rows = database.fetchall()
	return rows

if __name__ == "__main__":
	
	#setup the command line arguments create and empty
	for arg in sys.argv:
		if arg == "create":
			database_create()
		if arg == "empty":
			database_empty()
			
	database_close()


