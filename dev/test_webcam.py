#!/usr/bin/env python
#
#http://upgrayd.blogspot.com.au/2010/02/use-pygame-to-display-motion-jpeg.html 

import time
import httplib
import base64
import StringIO
import pygame
from pygame.locals import *

class WebStream:
    def __init__(self,ip,port='8090'):
        self.ip = ip
        self.port = port
        self.counter = 0

    def connect(self):
        h = httplib.HTTPConnection(self.ip,self.port,timeout=10)
        #h.request('GET','/?action=stream')
        #print self.counter
        h.request('GET','/?action=stream')
        #print h.getresponse()
        #errcode,errmsg,headers = h.getresponse()
        resp = h.getresponse()
        #print resp.status,resp.reason
        print resp.getheader('Content-Length')
        self.file = resp.read()
        #self.counter += 1

    def update(self,window,size,offset):
        #print self.file
        print 2
        buf = StringIO.StringIO(self.file)
        data = buf.readline()
        #data = self.file.readline()
        print data
        #if data[0:15] == 'Content-Length:':
            #count = int(data[16:])
        s = self.file.read()
        while s[0] != chr(0xFF):
            s = s[1:]

        p = StringIO.StringIO(s)

        try:
            campanel = pygame.image.load(p).convert()
            campanel = pygame.transform.scale(campanel,size)
            window.blit(campanel,offset)

        except Exception, x:
            print x

        p.close()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640,480),0,32)
    pygame.display.set_caption('WebStream Test')

    background = pygame.Surface((640,480))
    background.fill(pygame.Color('#E8E8E8'))
    screen.blit(background,(0,0))

    camera = WebStream('127.0.0.1','8090')
    camera.connect()

    while True:
        print 1
        camera.update(screen,(640,480),(0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

        time.sleep(0.1)

