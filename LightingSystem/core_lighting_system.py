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
from datetime import date, datetime
sys.path.append('../Configuration/')
sys.path.append('../Architecture/')
from light_core_configuration import configuration
from broker_configuration import broker_configuration
from LightingSystem import Lighting_System_Controller

#SYSTEM CORE INITIALITAZION#
try:

    building = Lighting_System_Controller(configuration['Building'],
                                          configuration['requested_lux'],
                                          configuration['timetable'])

    for i in range(len(configuration['Rooms'])):
        building.add_room(configuration['Rooms'][i]['name'],
                         configuration['Rooms'][i]['area'],
                         configuration['Rooms'][i]['length'],
                         configuration['Rooms'][i]['width'],
                         configuration['Rooms'][i]['height'])

        for light in configuration['Rooms'][i]['lights']:
            for k in range(light['zones']):
                building.rooms[i].add_lights(light['name'], 'Zone_'+str(k+1),
                    light['bulbs_per_zone'], light['max_lumen'])

    for room in building.rooms:
      room.show()
      for light in room.lights:
          light.show()

except:
    sys.exit('System Core Initialization failed')


def light_callback(client, userdata, msg):
  mes = json.loads(msg.payload)
  response = building.parse_light_message(mes, client)

  if response != None:
    client.publish(room.room_name+'/Light', json.dumps(response))

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("#")

def main():

    #BROKER CONNECTION#
    try:
        client = mqtt.Client()                
        client.connect(broker_configuration['IP'], broker_configuration['port'], 60)

        client.on_connect = on_connect

        client.message_callback_add('+/Light', light_callback)
        client.loop_start()
    except:
        sys.exit('Broker Connection failed')

    #LOOP
    while(True):

       building.check_status(client)

       time.sleep(500)

if __name__ == "__main__":
    main()