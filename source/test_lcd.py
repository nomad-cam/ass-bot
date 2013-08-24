#!/usr/bin/env python
#

import zmq
import time
import commands
import signal
import sys

interupt = False

def signal_handler(signum, frame):
    global interupt
    interupt = True


context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("ipc:///tmp/lcd.ipc")

i = 0
signal.signal(signal.SIGINT, signal_handler)

while True:
    eth0 = commands.getoutput("ifconfig eth0 | grep 'inet ' | awk '{ print $2 }'")
    wlan10 = commands.getoutput("ifconfig wlan10 | grep 'inet ' | awk '{ print $2 }'")
    print wlan10
    print eth0
    msg = {'message': eth0, 'line': '1', 'delay': '2'}
    
    print "sending message"
    zmq_socket.send_json(msg)

    if interupt:
        print("Shutting down script...")
        sys.exit()
        break

    print "sleeping 10"
    time.sleep(2)
    i = i + 1

sys.exit()
