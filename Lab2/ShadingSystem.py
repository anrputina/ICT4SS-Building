#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:31:21 2017

@author: anr.putina
"""

import math
from Room import Room 
from Sun import Sun
from datetime import date, datetime
from season_configuration import *

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

	def check_status(self):

		self.set_season(get_season(date.today()))
		self.set_season(get_season(date(2016, 6, 21)))

		self.sun.compute_elevation_azimuth()
		#self.sun.print_elevation_azimuth()

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
				angle = self.compute_winter_device_orientation(window)
				print ('set angle in winter to: ' + str(angle))
				window.set_angle(angle)

		else:
			print ('No Season recognized!')

	def compute_winter_device_orientation(self, window):

		if (-90 < self.sun.azimuth - window.window_azimuth < 90):
			angle = self.sun.azimuth - window.window_azimuth
		else:
			angle = 0
		
		return angle

	def compute_summer_device_orientation(self, window):

		w = compute_w_projection(window.device_width,	\
								 window.window_azimuth,	\
								 self.sun.azimuth,		\
								 window.angle)
		angle = window.angle

		if (window.window_azimuth > self.sun.azimuth):
			while ((w < window.device_width) and angle < 79):
				
				angle += 5 
				w = compute_w_projection(window.device_width,	\
										 window.window_azimuth,	\
										 self.sun.azimuth,		\
										 angle)

				print ('increasing angle to: '\
						+ str(angle) + 'and obtaining w: ' + str(w))

		else:
			while ( w < window.device_width and angle > -79):
				angle -= 5
				w = compute_w_projection(window.device_width,	\
										 window.window_azimuth,	\
										 self.sun.azimuth, 		\
										 abs(angle))
				print ('decreasing angle to: ' \
						+ str(angle) + 'and obtaining w: ' + str(w))

		return angle