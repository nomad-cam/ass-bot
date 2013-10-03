#!/usr/bin/env python
#

import zmq
import time
import commands

context = zmq.Context()
zmq_socket = context.socket(zmq.SUB)
zmq_socket.connect("ipc:///tmp/distance.ipc")
zmq_socket.setsockopt(zmq.SUBSCRIBE, '')

while True:
    #msg = {'leftA': '200', 'rightA': '300', 'leftV': '100', 'rightV': '50'}

    print "receiving message"
    print zmq_socket.recv_json()
    print "sleeping 10"
    time.sleep(10)
