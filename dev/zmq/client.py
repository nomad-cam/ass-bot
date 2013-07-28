#!/usr/bin/env python
#

import time
import zmq
context = zmq.Context()

work_receiver = context.socket(zmq.PULL)
work_receiver.connect("tcp://10.6.11.7:8875")

poller = zmq.Poller()
poller.register(work_receiver, zmq.POLLIN)

# Loop and accept messages from both channels, acting accordingly
while True:
    socks = dict(poller.poll(10))
    if socks:
        if socks.get(work_receiver) == zmq.POLLIN:
            print "got message ",work_receiver.recv(zmq.NOBLOCK)
    else:
        print "error: message timeout"
