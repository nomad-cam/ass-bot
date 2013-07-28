#!/usr/bin/env python
#

# This Beastie will receive all communication from mod_com.py

#import socket
import zmq
import time
import sys
import Device as dev
import Direction as dir

#initialise device
servo = dev.Device()
#set initial positions to neutral
neutral = [1500, 1500, 1500, 1500]
servo.set_targets(4,0,neutral)

def processCmd(message):
    global servo
    mes = message.split(':')
    if mes[1] == 'all':
        dir.stop_all(servo)
    if mes[1] == 'forward':
        dir.forward_all(servo,int(mes[2]))
    if mes[1] == 'reverse':
        dir.reverse_all(servo,int(mes[2]))
    if mes[1] == 'left':
        dir.turn_left(servo,int(mes[2]))
    if mes[1] == 'right':
        dir.turn_right(servo,int(mes[2]))


#http://stackoverflow.com/questions/7538988/zeromq-how-to-prevent-infinite-wait

context = zmq.Context()
sock_ipc = context.socket(zmq.SUB)
sock_ipc.bind('ipc://intercomm.ipc')
#Note can filter for specific messages...
sock_ipc.setsockopt(zmq.SUBSCRIBE, '' )

poller = zmq.Poller()
poller.register(sock_ipc, zmq.POLLIN)

while True:
    socks = dict(poller.poll(100))
    if socks:
        if socks.get(sock_ipc) == zmq.POLLIN:
            msg = sock_ipc.recv(zmq.NOBLOCK)
            print "Got message:",msg
            processCmd(msg)
    else:
        print "Error: message receive timeout"

