#!/usr/bin/env python
#

import time
import zmq
context = zmq.Context()

ventilator_send = context.socket(zmq.PUSH)
ventilator_send.bind("tcp://127.0.0.1:8875")

i=0

while True:
    i=i+1
    time.sleep(0.5)
    print ">>sending message ",i
    try:
        ventilator_send.send(repr(i),zmq.NOBLOCK)
        print "  succeed"
    except:
        print "  failed"
