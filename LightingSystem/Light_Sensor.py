#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:40:50 2017

@author: anr.putina
"""
import random

class Light_Sensor():

    def __init__(self, name, trace):
        self.name = name
        self.trace = trace
        # self.zone = zone    

    def get_lux(self, timestamp):
        #return random.randrange(400)
        return self.trace[timestamp]

    def show(self):
        print (self.name + ' in ' + self.zone)