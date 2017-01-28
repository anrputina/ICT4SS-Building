#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:31:21 2017

@author: anr.putina
"""

import paho.mqtt.client as mqtt
import json

WND_VAL = 0
WND_CNT = 2
TAB_VAL = 1
TAB_CNT = 3

import random

class Natural_light():
    
    def __init__(self):
#        self.natural_light = random.randint(0, 1200)
        self.natural_light = 40000
        
    def get_lux(self):
        return self.natural_light
    
    def set_lux(self):
        self.natural_light = eval(input('Insert the lux value'))
        return