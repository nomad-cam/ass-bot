#!/usr/bin/env python
#

# This Beastie will receive all communication from the control PC
# http://www.aonsquared.co.uk/the_dark_pi_rises

#import socket
import zmq
import time

#http://stackoverflow.com/questions/7538988/zeromq-how-to-prevent-infinite-wait

context = zmq.Context()
sock = context.socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, '')
sock.bind('tcp://*:8875')
# 10.6.11.7 asw120
# 10.6.0.72 assprobe01

#Forward instructions to specific module using ipc

sock_ipc = context.socket(zmq.PUB)
sock_ipc.connect('ipc://intercomm.ipc')
sock_ipc.setsockopt(zmq.HWM,1)


poller = zmq.Poller()
poller.register(sock, zmq.POLLIN)

while True:
    socks = dict(poller.poll(100))
    if socks:
        if socks.get(sock) == zmq.POLLIN:
            msg = sock.recv(zmq.NOBLOCK)
            print "Got message: ",msg
            try:
                sock_ipc.send(repr(msg),zmq.NOBLOCK)
            except:
                pass
    else:
        print "Error: message receive timeout"

