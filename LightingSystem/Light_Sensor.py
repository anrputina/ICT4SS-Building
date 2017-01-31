#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:40:50 2017

@author: anr.putina
"""

import random

max = 13
range(5, 22)

random.seed(1000000007)
values = [0, 0, 0, 0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0, 0, 0]
l = []

for x in values:
    if x == 0:
        l.append(x)
    
    elif x >= 0.1 and x <= 0.3:
        l.append(x * 25000 + random.randint(-1000, 1000))
        
    elif x >= 0.4 and x <= 0.6:
        l.append(x * 25000 + random.randint(-2000, 2000))
        
    elif x >= 0.6:
        l.append(x * 25000 + random.randint(-3000, 3000))


# import matplotlib.pyplot as plt
# plt.plot(l)
# plt.ylabel('some numbers')
# plt.show()

class Light_Sensor():

	def __init__(self, name, zone):
		self.name = name
		self.zone = zone    
        	
	def get_lux(self):
		return random.randrange(400)

	def show(self):
		print (self.name + ' in ' + self.zone)