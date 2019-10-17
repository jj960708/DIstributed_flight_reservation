# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 17:25:37 2019

@author: dingj
"""

import threading
import json
import socket
import sys
import os 
import pickle
from reservation import Event 
#container = sys.argv[1]


def hasRec(T,eR,i,j):
    return T[i][j] >= eR

## insert a event
def add(x):
    C += 1
    T[site_id][site_id] = C
    return 
    
 
    
    
    
def send_msg(sock,knownhosts,msg):
    msg = pickle.dumps(msg)
    
    for host in knownhosts['hosts']:
        if host == container:
            continue
        IP_address = knownhosts['hosts'][host]['ip_address'] 
        Port = int(knownhosts['hosts'][host]['udp_start_port'])
        sock.sendto(msg, (IP_address, Port))
        


def recv_msg(sock):
     while True:
        try:
            data,addr = sock.recvfrom(4096)
            data = pickle.loads(data)
            print(data)
            
        
        except:
            pass
    
    
container = sys.argv[1]
inputfile = open('knownhosts.json','r')
knownhosts = json.load(inputfile)
reservation_dic = [] ## dictionary to keep the local event
flight_info = [2 for i in range(20)] ## the local list to store the remaining seats of the flight

## determine the site ID
site_id = 0
C = 0 ##local clock
for host in range(len(knownhosts['hosts'])):
    if host == container:
        break
    site_id += 1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
UDP_address = knownhosts['hosts'][container]['ip_address'] 

UDP_PORT = int(knownhosts['hosts'][container]['udp_start_port'])
sock.bind((UDP_address, UDP_PORT))

t1 = threading.Thread(target=recv_msg,args=(sock,)).start()
while True:
    msg = input()
    
    if msg == 'Q':
        break
    if msg.startswith('reserve'):
        info = msg.split(' ')
        e = Event(C,info[1],site_id)
        for flight in info[2].split(','):
            e.flights.append(int(flight))
        temp = e.convert_to_string()
        print(temp)
        reservation_dic.append(e)
        print(e.time,e.client,e.flights)
        
        
    if msg == 'M':
        arr = [[1,2,3]]
        send_msg(sock,knownhosts,arr)
        
    else:
        
        send_msg(sock,knownhosts,msg)
    

sock.close()
os._exit(1)
