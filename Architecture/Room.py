#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:31:21 2017

@author: anr.putina
"""
import sys
import json
import datetime
sys.path.append('../LightingSystem')
from Window import Window
from Light_Sensor import Light_Sensor
from artificial_light import Artificial_light
import dweepy

class Room():

	def __init__(self, room_name, area, length, width, height):
		self.room_name = room_name
		self.area = area
		self.length = length
		self.width = width
		self.height = height
		self.windows = []
		self.lights = []
		self.light_sensors = []
		self.n_persons = 0

	def add_window(self, name, window_azimuth, height, length, device_number, device_width):
		new_window = Window(name, window_azimuth, height, length, device_number, device_width)
		self.windows.append(new_window)

	def add_lights(self, name, zone, bulbs_per_zone, max_lumen):
		new_ligth = Artificial_light(name, zone, bulbs_per_zone, max_lumen)
		self.lights.append(new_ligth)

	def add_light_sensor(self, name, zone):
		new_sensor = Light_Sensor(name, zone)
		self.light_sensors.append(new_sensor)

	def add_indoor_air_quality_parameters(self, qiaq,		\
										  ceiling_emission,	\
										  floor_emission,	\
										  wall_emission,	\
										  f_occupation,		\
										  wall_surface):
		self.requested_qiaq = qiaq
		self.ceiling_emission = ceiling_emission
		self.floor_emission = floor_emission
		self.wall_emission = wall_emission
		self.f_occupation = f_occupation
		self.wall_surface = wall_surface

	def request_person_number(self, client, timestamp):

		dict = {
				'name': self.room_name,
				'type': 'PIR-REQUEST',
				'timestamp': timestamp
				}

		try:
			client.publish(self.room_name+'/PIR', json.dumps(dict))
		except:
			'Error in publish request PIR'

	def set_number_persons(self, number_persons):
		self.n_persons = number_persons

	def reset_qiaq(self):
		self.qiaq = self.requested_qiaq

	def show(self):
		print(str(self.room_name)+' is: '+str(self.length)+'x'+str(self.width)+'x'+str(self.height))
		print('Has '+str(len(self.windows))+' and '+str(self.area)+'m^2')

	def request_lux_status(self, client, timestamp):
		
		dict = {
			'name': self.room_name,
			'type': 'LUX-REQUEST',
			'time': timestamp
		}

		try:
			client.publish(self.room_name+'/Light', json.dumps(dict))
		except:
			'Error in publish requests '

	def run_requested_qiaq(self, qiaq):
		self.requested_qiaq = qiaq

	def set_new_qiaq(self, qiaq):
		self.qiaq = qiaq

	def parse_air_message(self, msg):

		if(msg['type'] == 'COMMAND'):

			self.set_new_qiaq(msg['new_qiaq'])

			dict = {
				'name': self.room_name,
				'type': 'ACK',
				'new_qiaq': self.qiaq
			}

			return dict

		else:
			return None

	def parse_light_message(self, msg):

		if (msg['type'] == 'LUX-REQUEST'):
			dict = {
				'name': self.room_name,
				'type': 'RESPONSE',
				'time': msg['time']
			}

			for sensor in self.light_sensors:
				dict[sensor.name] = sensor.get_lux(msg['time'])

			return dict

		elif (msg['type'] == 'COMMAND'):
			
			dict = {
				'name': self.room_name,
				'type': 'ACK',
				'timestamp': msg['timestamp']
			}

			for light in self.lights:
				light.set_intensity_actuator(msg[light.name])
				dict[light.name] = light.get_intensity()
				dict[light.name+'_tot'] = light.get_intensity() * light.bulbs_per_zone
				dict[light.name+'_perc'] = round(float(light.get_intensity() * light.bulbs_per_zone)\
										 / (float(light.bulbs_per_zone*light.max_lumen)),2)

			return dict

		else:
			return None

	def parse_shade_message(self, msg):

		if (msg['type'] == 'COMMAND'):

			dict = {
				'name': self.room_name,
				'type': 'ACK',
				'timestamp': msg['timestamp']
			}

			for window in self.windows:
				window.set_motor_angle(msg[window.name])
				dict[window.name] = msg[window.name]

			print (dweepy.dweet_for('ICTBUILDINGPUTINASHADE',dict))

			return dict
		
		else:
			return None

	def create_shade_message(self, timestamp):

		dict = {
			'name': self.room_name,
			'type': 'COMMAND',
			'timestamp': timestamp
		}

		for window in self.windows:
			dict[window.name] = window.angle

		return dict