#!/usr/bin/env python
#

import zmq
import time
import commands

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.bind("ipc://lcd.ipc")

i = 0
while True:
    eth0 = commands.getoutput("ifconfig eth0 | grep 'inet ' | awk '{ print $2 }'")
    wlan10 = commands.getoutput("ifconfig wlan10 | grep 'inet ' | awk '{ print $2 }'")
    print wlan10
    print eth0
    msg = {'message': eth0, 'line': '1', 'delay': '10'}
    
    print "sending message"
    zmq_socket.send_json(msg)
    print "sleeping 10"
    time.sleep(10)
    i = i + 1
