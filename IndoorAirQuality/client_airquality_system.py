#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:42:07 2017

@author: anr.putina
"""

import sys
import math
sys.path.append('../Configuration/')
sys.path.append('../Architecture/')

import time
import json
import paho.mqtt.client as mqtt
from airquality_client_configuration import configuration
from broker_configuration import broker_configuration
from Room import Room

#Client INITIALITAZION#
try:
	room = Room(configuration['name'], configuration['area'],
				configuration['length'], configuration['width'],
				configuration['height'])
	
	room.run_requested_qiaq(configuration['requested_qiaq'])

	# room.add_indoor_air_quality_parameters(\
	# 	configuration['requested_qiaq'],
	# 	configuration['ceiling_emission'],
	# 	configuration['floor_emission'],
	# 	configuration['wall_emission'])
except:	
	sys.exit('System Core Initialization failed')

def air_quality_callback(client, userdata, msg):
	mes = json.loads(msg.payload)
	response = room.parse_air_message(mes)

	if response != None:
		client.publish(room.room_name+'/Air', json.dumps(response))
		print ('Publishing: ' + json.dumps(response))

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe(room.room_name+'/Air')

def main():

	#BROKER CONNECTION#
	try:
		client = mqtt.Client('client2')             	 
		client.connect(broker_configuration['IP'], broker_configuration['port'], 60)
		client.on_connect = on_connect

		client.message_callback_add(room.room_name+'/Air', air_quality_callback)
		client.loop_forever()

	except:
	 	sys.exit('Broker Connection failed')

if __name__ == "__main__":
	main()