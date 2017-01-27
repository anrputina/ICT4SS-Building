#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:31:21 2017

@author: anr.putina
"""

from Window import Window

class Room():

	def __init__(self, room_name, area, length, width, height):
		self.room_name = room_name
		self.area = area
		self.length = length
		self.width = width
		self.height = height
		self.windows = []

	def add_window(self, name,  window_azimuth, height, length, device_number, device_width):
		new_window = Window(name, window_azimuth, height, length, device_number, device_width)
		self.windows.append(new_window)

	def show(self):
		print(str(self.room_name)+' is: '+str(self.length)+'x'+str(self.width)+'x'+str(self.height))
		print('Has '+str(len(self.windows))+' and '+str(self.area)+'m^2')

	def read_message(self, msg):

		for window in self.windows:
			window.set_motor_angle(msg[window.name])

	def create_message(self):

		dict = {
			'name': self.room_name
		}

		for window in self.windows:
			dict[window.name] = window.angle

		return dict