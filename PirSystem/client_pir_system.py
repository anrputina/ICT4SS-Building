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
from PirSensor import Pir_Sensor
from broker_configuration import broker_configuration
from configuration_pir_system import configuration

#Client INITIALITAZION#
try:

	room = Pir_Sensor('Noisy_Working_Area')
	room.add_simulation_trace(configuration['traces'])

except:	
	sys.exit('System Core Initialization failed')

def PIR_callback(client, userdata, msg):
	mes = json.loads(msg.payload)
	response = room.get_person_number(mes)

	if response != None:
		client.publish(room.room_name+'/PIR', json.dumps(response))

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("#")

def main():

	#BROKER CONNECTION#
	try:
		client = mqtt.Client('clientpir')             	 
		client.connect(broker_configuration['IP'], broker_configuration['port'], 60)
		client.on_connect = on_connect

		client.message_callback_add(room.room_name+'/PIR', PIR_callback)
		client.loop_forever()
	except:
		sys.exit('Broker Connection failed')

if __name__ == "__main__":
	main()