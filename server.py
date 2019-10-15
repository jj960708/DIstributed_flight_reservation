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

#container = sys.argv[1]

def send_msg(sock,knownhosts,msg):
    
    
    for host in knownhosts['hosts']:
        if host == container:
            continue
        IP_address = knownhosts['hosts'][host]['ip_address'] 
        Port = int(knownhosts['hosts'][host]['udp_start_port'])
        sock.sendto(msg.encode('utf-8'), (IP_address, Port))


def recv_msg(sock):
     while True:
        try:
            data,addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass
    
    
container = sys.argv[1]
inputfile = open('knownhosts.json','r')
knownhosts = json.load(inputfile)



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
UDP_address = knownhosts['hosts'][container]['ip_address'] 
print(UDP_address)
UDP_PORT = int(knownhosts['hosts'][container]['udp_start_port'])
sock.bind((UDP_address, UDP_PORT))
t1 = threading.Thread(target=recv_msg,args=(sock,)).start()
while True:
    msg = input()
    if msg == 'Q':
        break
   
    send_msg(sock,knownhosts,msg)
    

sock.close()
os._exit(1)
