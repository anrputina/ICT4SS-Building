#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:31:21 2017

@author: anr.putina
"""

import sys
import json
import time
sys.path.append('../Architecture/')
from Room import Room 

import datetime
import time

import dweepy

class Indoor_Air_Quality_System():

	def __init__(self, name, timetable, voc_class_A):
		self.name = name
		self.timetable = timetable
		self.voc_class_A = voc_class_A
		self.rooms = []

	def add_room(self, room_name, area, length, width, height):
		new_room = Room(room_name, area, length, width, height)
		self.rooms.append(new_room)

	def check_requirement(self, room):

		if (room.n_persons>0):

			voc = self.compute_voc_value(room)

			while (voc > self.voc_class_A):
				room.set_new_qiaq(room.qiaq+5)
				voc = self.compute_voc_value(room)

		else:
			room.set_new_qiaq(0)
			print ('No persons in the room. Stop flow')

	def parse_pir_message(self, msg):
		if (msg['type'] == 'PIR-RESPONSE'):
			for room in self.rooms:
				if room.room_name == msg['name']:
					room.set_number_persons(msg['persons'])

	def compute_voc_value(self, room):

		surface_ceiling = room.length * room.width * 0.8418
		Volume = room.length * room.width * room.height

		ACH = (room.qiaq * room.n_persons / Volume)

		voc_floor = (room.floor_emission * room.length * room.width / (Volume * 0.9)) / ACH
		voc_ceiling = (room.ceiling_emission * surface_ceiling / (Volume * 0.9)) / ACH
		voc_wall = (room.wall_emission * room.wall_surface / (Volume * 0.9)) / ACH

		return (voc_floor + voc_ceiling + voc_wall)

	def check_status (self, client, timestamp):
		try:

			for room in self.rooms:
				room.request_person_number(client, str(timestamp))

			time.sleep(5)

			for room in self.rooms:
				room.reset_qiaq()
				self.check_requirement(room)

				print ('req soddis with qiaq: ' + str(room.qiaq))

				dict = {
					'name': room.room_name,
					'type': 'COMMAND',
					'new_qiaq': room.qiaq,
					'total_flow': room.qiaq * room.n_persons,
					'time': str(timestamp),
					'n_persons': room.n_persons
				}

				print (dweepy.dweet_for('ICTBUILDINGPUTINAPIR', dict))
				client.publish(room.room_name+'/Air', json.dumps(dict))

		except:
			print('')