#!/usr/bin/env python
#

import zmq
import time
import commands

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.bind("ipc:///tmp/motors.ipc")


while True:
    msg = {'leftA': '200', 'rightA': '300', 'leftV': '100', 'rightV': '50'}

    print "sending message"
    zmq_socket.send_json(msg)
    print "sleeping 10"
    time.sleep(10)
