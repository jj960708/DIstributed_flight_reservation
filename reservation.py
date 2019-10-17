# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 17:36:21 2019

@author: dingj
"""
## insert and delete algorithm
class Event:
    def __init__(self,time,clients,site_id):
        self.time = time
        self.client = clients
        self.status = 'pending'
        self.flights = []
        self.site_id = site_id
      
    ##serielizr the event class
    def convert_to_string(self):
        temp = str(self.time) + '+' + self.client +'+' + str(self.site_id) + '+'
        for f in self.flights:
            temp += str(f)
            temp += ','
            
        
        return temp[:-1]
    
    def construct_from_string(self,string):
        temp = string.split('+')
        self.time = int(temp[0])
        self.client = temp[1]
        self.site_id = int(temp[2])
        self.flights = [int(flight) for flight in temp[3].split(',')]
        
        