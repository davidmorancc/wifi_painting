#!/usr/bin/env python
#########################################################################################
#	gps_nmea																			#
#  	This utility converts gps formated in the NMEA GPGGA format to lat, long, and alt	#	
#	Other formats can easily be added using the pynmea library, I didn't have any need	#
#########################################################################################

from pynmea import nmea 	#need to install this

def convert_gpgga(line):

	gpgga = nmea.GPGGA()
	gpgga.parse(line)
	
	alt = gpgga.antenna_altitude
	lats = gpgga.latitude
	longs = gpgga.longitude

	#convert degrees,decimal minutes to decimal degrees 
	lat1 = (float(lats[2]+lats[3]+lats[4]+lats[5]+lats[6]+lats[7]+lats[8]))/60
	lat = (float(lats[0]+lats[1])+lat1)
	long1 = (float(longs[3]+longs[4]+longs[5]+longs[6]+longs[7]+longs[8]+longs[9]))/60
	long = (float(longs[0]+longs[1]+longs[2])+long1)

	#calc position
	pos_y = lat
	pos_x = -long 		#longitude is negaitve

	return [pos_y, pos_x, alt]
	
if __name__ == "__main__":

	#sample data
	line = "$GPGGA,031637,4219.20826,N,07106.28325,W,1,8,0.9,17.8,M,46.9,M,0,2*58"
	
	print convert_gpgga(line)
