#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:31:22 2017

@author: anr.putina
"""

class Window():

	def __init__(self, name, window_azimuth, height, length, device_number, device_width):
		self.name = name
		self.window_azimuth = window_azimuth
		self.height = height
		self.length = length
		self.device_number = device_number
		self.device_width = device_width
		self.angle = 0

	def set_angle(self, angle):
		self.angle = angle

	def set_motor_angle(self, angle):
		self.angle = angle

	def show(self):
		print(self.name)
		print('The orientation of the window is: '+str(self.window_azimuth)+' degree')
		print('Height: '+ str(self.height)+', Length: '+str(self.length))
		print('Device number: '+str(self.device_number)+', Device width: '+str(self.device_width))