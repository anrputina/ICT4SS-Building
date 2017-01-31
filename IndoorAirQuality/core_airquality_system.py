#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:42:07 2017

@author: anr.putina
"""

import sys
import time
import json
import paho.mqtt.client as mqtt
# from datetime import date, datetime
import datetime
sys.path.append('../Configuration/')
sys.path.append('../Architecture/')
from broker_configuration import broker_configuration
from airquality_core_configuration import configuration
from IndoorAirQuality import Indoor_Air_Quality_System
import time
#SYSTEM CORE INITIALITAZION#
try:
	building = Indoor_Air_Quality_System(configuration['Building'],
										 configuration['timetable'],
										 configuration['voc_class_A'])

	for i in range(len(configuration['Rooms'])):
		building.add_room(configuration['Rooms'][i]['name'],
						 configuration['Rooms'][i]['area'],
						 configuration['Rooms'][i]['length'],
						 configuration['Rooms'][i]['width'],
						 configuration['Rooms'][i]['height'])
  
		building.rooms[i].add_indoor_air_quality_parameters(\
			configuration['Rooms'][i]['requested_qiaq'],
			configuration['Rooms'][i]['ceiling_emission'],
			configuration['Rooms'][i]['floor_emission'],
			configuration['Rooms'][i]['wall_emission'],
			configuration['Rooms'][i]['f_occupation'],
			configuration['Rooms'][i]['wall_surface'])
	
except:
	sys.exit('System Core Initialization failed')

def pir_callback(client, userdata, msg):
	mes = json.loads(msg.payload)
	response = building.parse_pir_message(mes)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("#")

def main():

    # BROKER CONNECTION#
    try:
        client = mqtt.Client('clientcore')                
        client.connect(broker_configuration['IP'], broker_configuration['port'], 60)

        client.on_connect = on_connect
        client.message_callback_add('+/PIR', pir_callback)

        client.loop_start()
    except:
        sys.exit('Broker Connection failed')

    #LOOP
    while(True):

    	for hour in range(0, 24, 1):

			timestamp = datetime.datetime(2017, 1, 1, hour, 0, 0)
			# timestamp = datetime.date().now()
			print timestamp
			# now = timestamp.time()

			# if now >= time(building.timetable[0], building.timetable[1]) \
			# 	and now <= time(building.timetable[2],building.timetable[3]):

			if hour >= building.timetable[0] and hour <= building.timetable[2]:
				building.check_status(client, timestamp)
				print ('sleep 10 seconds ')

			else:
				print 'NIGHT, no need for ACH'

			time.sleep(3)

if __name__ == "__main__":
    main()