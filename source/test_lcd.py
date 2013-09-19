#!/usr/bin/env python
#

import time
import commands
import signal
import sys
import zmq

interupt = False

def signal_handler(signum, frame):
    global interupt
    interupt = True


context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("ipc:///tmp/lcd.ipc")

signal.signal(signal.SIGINT, signal_handler)

while True:
    eth0 = commands.getoutput("ifconfig eth0 | grep 'inet ' | awk '{ print $2 }'")
    wlan10 = commands.getoutput("ifconfig wlan10 | grep 'inet ' | awk '{ print $2 }'")
    #print wlan10
    #print eth0
    msg = {'message': 'Are you there?', 'line': '0'}
    
    print("sending message %s", msg)
    zmq_socket.send_json(msg)

    if interupt:
        print("Shutting down script...")
        sys.exit()
        break

    print("sleeping 5")
    time.sleep(5)

sys.exit()
