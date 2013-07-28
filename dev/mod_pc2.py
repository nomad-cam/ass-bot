#!/usr/bin/env python
#

# PC control module.
#
# The base station communications will all be sent through this module...
# Will use pygame for input control support (keyboard, joystick, digipot, etc

import socket
import time
import pygame
from pygame.locals import *

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Init Sockets
#

s = socket.socket() #Create the Socket
host = '10.6.0.164'   #set the robot ip connection
port = 8888         #set the comand port

s.connect((host,port))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Init Pygame
#

pygame.init()

screen = pygame.display.set_mode((640,480),16)
pygame.display.set_caption('Move you ASS')
pygame.mouse.set_visible(0)

pygame.key.set_repeat(1,200)

MAXFPS = 20
clock = pygame.time.Clock()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Start Main
#

done = False
while not done:
    #image = webcam.get_image()
    #screen.blit(image,(0,0))
    #pygame.display.update()

    for event in pygame.event.get():
        #if (event.type == KEYUP) or (event.type == KEYDOWN):
        if (event.type == KEYDOWN):
        #while (event.type == KEYDOWN):
            #print event
            if (event.type == pygame.QUIT):
                done = True
            if (event.key == K_ESCAPE):
                done = True
            if (event.key == K_LEFT):
                print "Turning left"
                s.send('left,20')
                #dir.turn_left(servo,20)
            if (event.key == K_RIGHT):
                print "Turning right"
                s.send('right,20')
                #dir.turn_right(servo,20)
            if (event.key == K_UP):
                print "Moving ahead"
                s.send('forward,20')
                #dir.forward_all(servo,20)
            if (event.key == K_DOWN):
                print "Reversing... Beep... Beep..."
                s.send('reverse,20')
                #dir.reverse_all(servo,20)
            if (event.key ==K_SPACE):
                s.send('stop,0')
                #dir.stop_all(servo)

    clock.tick(MAXFPS)

s.close()
