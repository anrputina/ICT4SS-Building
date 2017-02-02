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
from Room import Room 
from Sun import Sun
from datetime import date, datetime
from season_configuration import *

import dweepy

def compute_w_projection(device_length, window_azimuth, solar_azimuth, angle):

	if (window_azimuth > solar_azimuth):
		w = device_length * (math.sin(math.radians(angle)) \
			+ math.cos(math.radians(angle)) \
			* math.tan(math.radians(window_azimuth) \
			- math.radians(solar_azimuth)))
	else:
		w = abs(device_length * (math.sin(math.radians(angle)) \
			+ math.cos(math.radians(angle)) \
			* math.tan(math.radians(window_azimuth) \
			- math.radians(solar_azimuth))))
	return w

class Shading_System_Controller():

	def __init__(self, name, season, latitude, longitude):
		self.name = name
		self.sun = Sun(latitude, longitude)
		self.season = season
		self.rooms = []
		self.dweet = 'ICTBUILDINGPUTINASHADE'

	def set_season(self, season):
		self.season = season

	def add_room(self, room_name, area, length, width, height):
		new_room = Room(room_name, area, length, width, height)
		self.rooms.append(new_room)

	def compute_statistics(self, window):
		if (self.sun.elevation > 0 and window.window_azimuth - 90 
			< self.sun.azimuth < window.window_azimuth + 90):
			w = compute_w_projection(window.device_width,\
									 window.window_azimuth,\
									 self.sun.azimuth,\
									 window.angle)

			print ('Each device covers: ' + str(w))
			print ('Number of devices: ' + str (window.device_number))
			print ('Covering in total:' \
					+ str((window.device_number * w * window.height)\
					/(window.length*window.height)*100) + '%' )
		else:
			print('No need to Shade window with '+str(window.window_azimuth)+' degree in azimuth')

	def check_status(self, timestamp):

		# self.set_season(get_season(date.today()))
		self.set_season(get_season(timestamp.date()))
		self.sun.compute_elevation_azimuth(timestamp)
		self.sun.print_elevation_azimuth()

		for i in range(len(self.rooms)):
			for window in self.rooms[i].windows:

				if (window.window_azimuth - 90 < self.sun.azimuth < window.window_azimuth + 90):
					self.compute_device_orientation(window)
				else:
					window.set_angle(0)

				self.compute_statistics(window)
				#print (window.window_azimuth)

	def compute_device_orientation(self, window):

		if self.season == 'Summer':
			
			if self.sun.elevation < 0:
				window.set_angle(0)
			else:
				angle = self.compute_summer_device_orientation(window)
				print ('set angle in summer to: ' + str(angle))
				window.set_angle(angle)

		elif self.season == 'Winter':
			
			if self.sun.elevation < 0:
				window.set_angle(0)
			else:
				angle = int(self.compute_winter_device_orientation(window))
				print ('set angle in winter to: ' + str(angle))
				window.set_angle(angle)

		else:
			print ('No Season recognized!')

	def compute_winter_device_orientation(self, window):

		# if (-90 < self.sun.azimuth - window.window_azimuth < 90):
		# 	angle = self.sun.azimuth - window.window_azimuth
		# else:
		# 	angle = 0
		
		# return angle
		return self.sun.azimuth - window.window_azimuth

	def compute_summer_device_orientation(self, window):

		w = compute_w_projection(window.device_width,	\
								 window.window_azimuth,	\
								 self.sun.azimuth,		\
								 window.angle)
		angle = window.angle

		if (window.window_azimuth > self.sun.azimuth):
			# while ((w < window.device_width) and angle < 79):
				
			# 	# angle += 5 

			# 	# w = compute_w_projection(window.device_width,	\
			# 	# 						 window.window_azimuth,	\
			# 	# 						 self.sun.azimuth,		\
			# 	# 						 angle)

			# 	# print ('increasing angle to: '\
			# 	# 		+ str(angle) + 'and obtaining w: ' + str(w))
			angles=[]
			for angle in range (0, 80, 5):
				angles.append(compute_w_projection(window.device_width,	\
									 window.window_azimuth,				\
									 self.sun.azimuth,					\
									 angle))

			return angles.index(max(angles))*5



		else:
			# angle = 0
			# while ( w < window.device_width and angle > -79):
				# angle -= 5
				# w = compute_w_projection(window.device_width,	\
				# 						 window.window_azimuth,	\
				# 						 self.sun.azimuth, 		\
				# 						 abs(angle))
				# print ('decreasing angle to: ' \
				# 		+ str(angle) + 'and obtaining w: ' + str(w))

			angles = []
			for angle in range (-80, 0, 5):
				angles.append(compute_w_projection(window.device_width,	\
									 window.window_azimuth,				\
									 self.sun.azimuth,					\
									 abs(angle)))

			return angles.index(min(angles))*(-5)

	def parse_shade_message(self, msg):

		if (msg['type'] == 'ACK'):
			print (dweepy.dweet_for(self.dweet, msg))
		else:
			pass