#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:31:21 2017

@author: anr.putina
"""

import sys
import math
sys.path.append('../Configuration/')
sys.path.append('../Architecture/')
import time
import json
import paho.mqtt.client as mqtt
from shade_client_configuration import configuration
from broker_configuration import broker_configuration
from Room import Room

#Client INITIALITAZION#
try:

	room = Room(configuration['name'],
				configuration['area'],
				configuration['length'],
				configuration['width'],
				configuration['height'])

	for window in configuration['windows']:
		room.add_window(window['name'],window['azimuth'], window['height'],
		  window['length'], window['device_number'], window['device_width'])

	# for window in room.windows:
	# 	window.show()

except:
	sys.exit('System Core Initialization failed')

def shade_callback(client, userdata, msg):
	mes = json.loads(msg.payload)
	response = room.parse_shade_message(mes)

	if response != None:
		client.publish(room.room_name+'/Shade', json.dumps(response))
		print ('Publishing: ' + json.dumps(response))

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("#")

def main():

	#BROKER CONNECTION#
	try:
		client = mqtt.Client()             	 
		client.connect(broker_configuration['IP'], broker_configuration['port'], 60)
		client.on_connect = on_connect

		client.message_callback_add(room.room_name+'/Shade', shade_callback)
		client.loop_forever()
	except:
		sys.exit('Broker Connection failed')

if __name__ == "__main__":
	main()