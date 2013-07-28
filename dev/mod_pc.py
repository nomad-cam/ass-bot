#!/usr/bin/env python
#

# PC control module.
#
# The base station communications will all be sent through this module...
# Will use pygame for input control support (keyboard, joystick, digipot, etc

# http://code.google.com/p/mjpeg-stream-client/

import httplib    #httplib modules for the HTTP interactions
import zmq
import sys
import json
from Tkinter import * #Tkinter modules for Windowing
import tkMessageBox
from PIL import Image, ImageTk #Python Image Libraries, required for displaying jpegs
from time import sleep
import StringIO                 #For converting Stream from the server to IO for Image (PIL)
from StreamViewer import StreamViewer           

if len(sys.argv) < 2:
     print "Usage: %s [host]" % sys.argv[0]
     sys.exit(100)

context = zmq.Context()
data_send = context.socket(zmq.PUSH)
connecto = "%s%s%s" % ("tcp://",sys.argv[1],":8875")
print connecto
data_send.bind(connecto)


def zmqSend(data):
     try:
          data_send.send(repr(data),zmq.NOBLOCK)
     except:
          # Failed to send... ignore and wait for new request
          pass

         
'''Gets the file from the specified
host, port and location/query'''
def get(host,port,query):
     #give priority to command line argument host
     if len( sys.argv ) > 1:
          host = sys.argv[1]
     h = httplib.HTTP(host, port)
     h.putrequest('GET', query)
     h.putheader('Host', host)
     h.putheader('User-agent', 'python-httplib')
     h.putheader('Content-type', 'image/jpeg')
     h.endheaders()
     
     (returncode, returnmsg, headers) = h.getreply()
     #print "return code:",returncode
     #print "return message:",returnmsg
     #print "headers:",headers
     if returncode != 200:
         print returncode, returnmsg
         sys.exit()
     
     f = h.getfile()
     return f.read()

'''This is where we show the file on our StreamViewer'''
def streamfile(tbk, root):
     #f = get('127.0.0.1',80,'/?action=snapshot')
     f = get('10.6.0.72',8090,'/?action=snapshot')
     #f = get(port=8090,query='/?action=snapshot')
     img=Image.open(StringIO.StringIO(f)) #convert to jpeg object from the stream
     imagetk = ImageTk.PhotoImage(img) #Get a PhotoImage to pass to our Frame
     tbk.addImage(imagetk) #Image added
     root.update()


def keypress(event):
     if event.keysym == 'Escape':
          really_delete()
     x = event.char
     y = event.keysym
     if x.lower() == "w":
          print "www"
     if x.lower() == "a":
          print "aaa"
     if x.lower() == "s":
          print "sss"
     if x.lower() == "d":
          print "ddd"
     if y == "Left":
          print "left"
     if y == "Right":
          print "right"
     if y == "Up":
          print "Up"
     if y == "Down":
          print "Down"
     if y == "space":
          print "Shutdown sequence initiated"
     else:
          print "argh",x,event.keycode,event.keysym
     

def really_delete():
     if tkMessageBox.askokcancel("Quit","Press OK for work and worry... \nPress Cancel for guns and glory"):
          root.destroy()


root = Tk()
root.bind_all('<Key>', keypress)
root.protocol("WM_DELETE_WINDOW", really_delete)

tbk = StreamViewer(root)
#As much space as we need, no more, no less
#we change the root geometry to the size of the streaming jpg #As much space as we need, no more, no less

root.geometry("%dx%d+0+0" % (1280, 720))
root.resizable(False,False)
'''It's our overrated slideshow viewer .. hehe'''
while(1):
     streamfile(tbk,root)
