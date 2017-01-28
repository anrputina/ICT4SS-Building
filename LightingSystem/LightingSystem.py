#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:31:21 2017

@author: anr.putina
"""

import sys
import json
sys.path.append('../Architecture/')
from Room import Room 

from datetime import datetime, time

class Lighting_System_Controller():

	def __init__(self, name, requested_lux, timetable):
		self.name = name
		self.requested_lux = requested_lux
		self.timetable = timetable
		self.rooms = []

	def add_room(self, room_name, area, length, width, height):
		new_room = Room(room_name, area, length, width, height)
		self.rooms.append(new_room)

	def check_status(self, client):

		now = datetime.now().time()
		if now >= time(self.timetable[0], self.timetable[1]) \
			and now <= time(self.timetable[2],self.timetable[3]):

			for room in self.rooms:
				room.request_lux_status(client)

		else:
			print('IT S NIGHT! GO TO SLEEP!')

	def check_light_requirement(self, lux_value):

		if (lux_value > self.requested_lux):
			return 0
		else:
			return (self.requested_lux-lux_value)/self.requested_lux

	def parse_light_message(self, msg, client):

		if (msg['type'] == 'RESPONSE'):
			for room in self.rooms:
				if room.room_name == msg['name']:
					dict = {
						'name': room.room_name,
						'type': 'COMMAND'
					}
					for light in room.lights:
						light.set_intensity(self.check_light_requirement(msg[light.zone]))
						dict[light.zone] = light.get_intensity()
					client.publish(room.room_name+'/Light', json.dumps(dict))
					break
				else:
					'Don t have this room in process'

		elif (msg['type'] == 'ACK'):
			pass

		else:
			pass