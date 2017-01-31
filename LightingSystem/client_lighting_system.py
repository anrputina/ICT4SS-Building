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
from light_client_configuration import configuration
from broker_configuration import broker_configuration
from light_sensor_configuration import configuration_light_sensor
from Room import Room

#Client INITIALITAZION#
try:
	room = Room(configuration['name'],
				configuration['area'],
				configuration['length'],
				configuration['width'],
				configuration['height'])

	for light in configuration['lights']:
		for k in range(light['zones']):
			room.add_lights(light['name'], 'Zone_'+str(k+1),
			light['bulbs_per_zone'], light['max_lumen'])

	# for sensor in configuration['sensors']:
	# 	for k in range(sensor['zones']):
	# 		room.add_light_sensor(sensor['name']+'_'+str(k+1),
	# 							 'Zone_'+str(k+1))

	for sensor in configuration['sensors']:
		room.add_light_sensor(sensor['name'], configuration_light_sensor['trace'])

	# for light in room.lights:
	# 	light.show()
	# for sensor in room.sensors:
	# 	sensor.show()

except:	
	sys.exit('System Core Initialization failed')


def light_callback(client, userdata, msg):
	mes = json.loads(msg.payload)
	response = room.parse_light_message(mes)

	if response != None:
		client.publish(room.room_name+'/Light', json.dumps(response))
		print ('Publishing: ' + json.dumps(response))

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("#")

def main():

	#BROKER CONNECTION#
	try:
		client = mqtt.Client('client-light')             	 
		client.connect(broker_configuration['IP'], broker_configuration['port'], 60)
		client.on_connect = on_connect

		client.message_callback_add(room.room_name+'/Light', light_callback)
		client.loop_forever()
	except:
		sys.exit('Broker Connection failed')

if __name__ == "__main__":
	main()