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
def insert(client,flights):
    global C,T
    C += 1
    T[site_id][site_id] = C
    e = Event(C,client,site_id,'insert')
    e.flights =[int(f) for f in flights.split(',')]
    partial_log.append(e)
    reservation_dic[client] = e.flights 
    return 

def delete(client,flights):
    global C,T
    C += 1
    T[site_id][site_id] = C
    e = Event(C,client,site_id,'delete')
    e.flights =[int(f) for f in flights.split(',')]
    partial_log.append(e)
    reservation_dic.pop(client)
    return 
    
 
    
    

def send_msg(sock,knownhosts,site,msg):
    msg = pickle.dumps(msg)
    IP_address = knownhosts['hosts'][site]['ip_address'] 
    Port = int(knownhosts['hosts'][site]['udp_start_port'])
    sock.sendto(msg, (IP_address, Port))
    
def send_all(sock,knownhosts,msg):
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
reservation_dic = {} ## dictionary to keep the local event
partial_log = []
flight_info = [2 for i in range(20)] ## the local list to store the remaining seats of the flight
T = [[0 for i in range(2)] for i in range(2)]
## determine the site ID
site_id = int(sys.argv[2])
C = 0 ##local clock


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
UDP_address = knownhosts['hosts'][container]['ip_address'] 

UDP_PORT = int(knownhosts['hosts'][container]['udp_start_port'])
sock.bind((UDP_address, UDP_PORT))

t1 = threading.Thread(target=recv_msg,args=(sock,)).start()
while True:
    msg = input()
    
    if msg == 'Q':
        break
    elif msg.startswith('reserve'):
        info = msg.split(' ')
        
        insert(info[1],info[2])
        print(reservation_dic,C)
        
    elif msg.startswith('send'):
        sent_to = msg.split(' ')[1]
        send_msg(sock,knownhosts,sent_to,msg)
    
        
        
    elif msg.startswith('sendall'):
        
        send_all(sock,knownhosts,msg)
    

sock.close()
os._exit(1)
