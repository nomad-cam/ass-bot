#!/usr/bin/env python
#
#

import Device as device

####################
##    Remember    ##
# ---------------- #
# S0 = front left  #
# S1 = back left   #
# S2 = front right #
# S3 = back right  #
####################

# requires Device object and rate...
def turn_left(servo, rate, fl=0, bl=1, fr=2, br=3):

    #Get the current position...
    cur_pos_left = servo.get_positions([fl,bl])
    cur_pos_right = servo.get_positions([fr,br])
    print cur_pos_left, cur_pos_right
    print abs(sum(cur_pos_left)),abs(sum(cur_pos_right))

    # If stationary spin on spot...
    if abs(sum(cur_pos_left)) == abs(sum(cur_pos_right)):
        new_pos_left = [x - rate for x in cur_pos_left]
        new_pos_right = [x - rate for x in cur_pos_right]
    # else calculate turn on current movement
    else:
        new_pos_left = cur_pos_left
        new_pos_right = [x - rate for x in cur_pos_right]
    
    servo.set_targets(4,fl,new_pos_left+new_pos_right)


def turn_right(servo, rate, fl=0, bl=1, fr=2, br=3):
    #Get the current position...
    cur_pos_left = servo.get_positions([fl,bl])
    cur_pos_right = servo.get_positions([fr,br])
    print cur_pos_left, cur_pos_right
    #print abs(sum(cur_pos_left)),abs(sum(cur_pos_right))

    # If stationary spin on spot...
    if abs(sum(cur_pos_left)) == abs(sum(cur_pos_right)):
        new_pos_left = [x + rate for x in cur_pos_left]
        new_pos_right = [x + rate for x in cur_pos_right]
    # else calculate turn on current movement
    else:
        new_pos_left = cur_pos_left
        new_pos_right = [x + rate for x in cur_pos_right]

    servo.set_targets(4,fl,new_pos_left+new_pos_right)


def forward_all(servo, rate, fl=0, bl=1, fr=2, br=3):
    #Get the current position...
    cur_pos_left = servo.get_positions([fl,bl])
    cur_pos_right = servo.get_positions([fr,br])

    new_pos_left = [x + rate for x in cur_pos_left]
    new_pos_right = [x - rate for x in cur_pos_right]

    servo.set_targets(4,fl,new_pos_left+new_pos_right)


def reverse_all(servo, rate, fl=0, bl=1, fr=2, br=3):
    #Get the current position...
    cur_pos_left = servo.get_positions([fl,bl])
    cur_pos_right = servo.get_positions([fr,br])

    new_pos_left = [x - rate for x in cur_pos_left]
    new_pos_right = [x + rate for x in cur_pos_right]

    servo.set_targets(4,fl,new_pos_left+new_pos_right)


def stop_all(servo,fl=0):
    servo.set_targets(4,fl,[1500,1500,1500,1500])
