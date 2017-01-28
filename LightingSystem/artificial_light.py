#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:39:08 2017

@author: anr.putina
"""

class Artificial_light:
    
    def __init__(self, name, zone, bulbs_per_zone, max_lumen):
        self.name = name
        self.zone = zone
        self.bulbs_per_zone = bulbs_per_zone
        self.max_lumen = max_lumen
        self.intensity = 0 #Off by default
        
    def get_intensity(self):
        return self.intensity
                    
    def set_intensity(self, intensity):
        self.intensity = intensity

    def set_intensity_actuator(self, intensity):
        self.intensity = intensity

    def show(self):
        print(self.name + ' in ' + self.zone)
        print ('#'+str(self.bulbs_per_zone) + ' with max:' +str(self.max_lumen)+' lumen')