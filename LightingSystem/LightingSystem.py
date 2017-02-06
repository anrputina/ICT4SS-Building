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

from datetime import datetime
import time

import dweepy


class Lighting_System_Controller():

	def __init__(self, name, requested_lux, timetable):
		self.name = name
		self.requested_lux = requested_lux
		self.timetable = timetable
		self.rooms = []
		self.dweep = 'ICTBUILDINGPUTINALIGHT'

	def add_room(self, room_name, area, length, width, height):
		new_room = Room(room_name, area, length, width, height)
		self.rooms.append(new_room)

	def check_status(self, client, timestamp):

		#WITH REAL VALUES IN TIMESTAMP
		# now = datetime.now().time()
		# if now >= time(self.timetable[0], self.timetable[1]) \
		# 	and now <= time(self.timetable[2],self.timetable[3]):

		# 	for room in self.rooms:
		# 		room.request_lux_status(client)

		# else:
		# 	print('IT S NIGHT! GO TO SLEEP!')

		for room in self.rooms:
			room.request_person_number(client, str(timestamp))

		time.sleep(5)

		#SIMULATING PART!

		for room in self.rooms:
			room.request_lux_status(client, timestamp.hour)

	def down_all(self, client, timestamp):
		for room in self.rooms:

			dict = {
				'name': room.room_name,
				'type': 'COMMAND',
				'timestamp': str(timestamp)
			}

			for light in room.lights:
				light.set_intensity(0)
				dict[light.name] = 0

			try:
				client.publish(room.room_name+'/Light', json.dumps(dict))
			except:
				print 'Impossible to publish Light message'


	def check_light_requirement(self, lux_value, room):

		lux = lux_value * 0.0254
		flux = lux * room.area

		if (flux > self.requested_lux):
			return 0
		else:
			needed_lux = self.requested_lux - flux
			flux_per_zone = needed_lux / len(room.lights)

			for light in room.lights:
				final_per_bulb = flux_per_zone / light.bulbs_per_zone

			return (int(final_per_bulb))

	def parse_pir_message(self, msg):
		if (msg['type'] == 'PIR-RESPONSE'):
			for room in self.rooms:
				if room.room_name == msg['name']:
					room.set_number_persons(msg['persons'])

	def parse_light_message(self, msg, client):

		if (msg['type'] == 'RESPONSE'):
			for room in self.rooms:
				if room.room_name == msg['name']:
					
					dict = {
						'name': room.room_name,
						'type': 'COMMAND',
						'timestamp': msg['time']
					}

					if room.n_persons > 0:

						for light in room.lights:
							light.set_intensity(self.check_light_requirement(msg['Light-Sensor'], room))
							dict[light.name] = light.get_intensity()

					else:
						for light in room.lights:
							light.set_intensity(0)
							dict[light.name] = 0

					client.publish(room.room_name+'/Light', json.dumps(dict))
					break

				else:
					'Don t have this room in process'

		elif (msg['type'] == 'ACK'):
			print (dweepy.dweet_for(self.dweep, msg))

		else:
			pass