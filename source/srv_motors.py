#!/usr/bin/env python

""" srv_motors.py: Receive commands to control 2 phidgets motors"""

"""
Borrowed and modified from the phidgets example code by Adam Stelmack
http://creativecommons.org/licenses/by/2.5/ca/
"""



#Basic imports
from ctypes import *
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, CurrentChangeEventArgs, InputChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.MotorControl import MotorControl
#import methods for sleeping thread
from time import sleep

import zmq


#Create an motorcontrol object
try:
    motorControlL = MotorControl() # Left Motor
    motorControlR = MotorControl() # Right Motor
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (motorControlL.isAttached(), motorControlL.getDeviceName(), motorControlL.getSerialNum(), motorControlL.getDeviceVersion()))
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (motorControlR.isAttached(), motorControlR.getDeviceName(), motorControlR.getSerialNum(), motorControlR.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")

#Event Handler Callback Functions
def motorControlAttached(e):
    attached = e.device
    print("MotorControl %i Attached!" % (attached.getSerialNum()))

def motorControlDetached(e):
    detached = e.device
    print("MotorControl %i Detached!" % (detached.getSerialNum()))

def motorControlError(e):
    try:
        source = e.device
        print("Motor Control %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def motorControlCurrentChanged(e):
    source = e.device
    print("Motor Control %i: Motor %i Current Draw: %f" % (source.getSerialNum(), e.index, e.current))

def motorControlInputChanged(e):
    source = e.device
    print("Motor Control %i: Input %i State: %s" % (source.getSerialNum(), e.index, e.state))

def motorControlVelocityChanged(e):
    source = e.device
    print("Motor Control %i: Motor %i Current Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))

#Main Program Code
#try:
#    motorControlL.setOnAttachHandler(motorControlAttached)
#    motorControlL.setOnDetachHandler(motorControlDetached)
#    motorControlL.setOnErrorhandler(motorControlError)
#    motorControlL.setOnCurrentChangeHandler(motorControlCurrentChanged)
#    motorControlL.setOnInputChangeHandler(motorControlInputChanged)
#    motorControlL.setOnVelocityChangeHandler(motorControlVelocityChanged)

#    motorControlR.setOnAttachHandler(motorControlAttached)
#    motorControlR.setOnDetachHandler(motorControlDetached)
#    motorControlR.setOnErrorhandler(motorControlError)
#    motorControlR.setOnCurrentChangeHandler(motorControlCurrentChanged)
#    motorControlR.setOnInputChangeHandler(motorControlInputChanged)
#    motorControlR.setOnVelocityChangeHandler(motorControlVelocityChanged)

#except PhidgetException as e:
#    print("Phidget Exception %i: %s" % (e.code, e.details))
#    print("Exiting....")
#    exit(1)

print("Opening phidget object....")

try:
    motorControlL.openPhidget()
    motorControlR.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    motorControlL.waitForAttach(10000)
    motorControlR.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        motorControlL.closePhidget()
        motorControlR.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

#print(motorControlL.getAccelerationMin(0))
#print(motorControlR.getAccelerationMin(0))
#print(motorControlL.getAccelerationMax(0))
#print(motorControlR.getAccelerationMax(0))

print("Press Enter to continue....")
chr = sys.stdin.read(1)

context = zmq.Context()
motors_receiver = context.socket(zmq.PULL)
motors_receiver.connect("ipc:///tmp/motors.ipc")

# messages passed in as {left acc, left vel, right acc, right vel, rel}
# velocity: -100 to 100; 0 is stop
# acceleration: AccMin(24.51) to AccMax (6250)
# rel: relative or absolute settings

while True:
    print("Going into forever loop mode")
    result = motors_receiver.recv_json()
    print(result)

    if 'rel' in result:
        print("Relative Settings...")
        try:
            lar = motorControlL.getAcceleration(0)
            rar = motorControlR.getAcceleration(0)

            lvr = motorControlL.getAcceleration(0)
            rvr = motorControlR.getAcceleration(0)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

        try:
            motorControlL.setAcceleration(0, (int(result['leftA']) + lar) )
            motorControlR.setAcceleration(0, (int(result['rightA']) + rar) )
            motorControlL.setVelocity(0, (int(result['leftV']) + lvr) )
            motorControlR.setVelocity(0, (int(result['rightV']) + rvr) )
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

    else:
        print("Absolute Settings...")
        try:
            motorControlL.setAcceleration(0, int(result['leftA']))
            motorControlR.setAcceleration(0, int(result['rightA']))
            motorControlL.setVelocity(0, int(result['leftV']))
            motorControlR.setVelocity(0, int(result['rightV']))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
    
#Control the motor a bit.
#print("Will now simulate motor operation....")
#print("Step 1: increase acceleration to 50, set target speed at 100")
#try:
#    motorControlL.setAcceleration(0, 50.00)
#    motorControlR.setAcceleration(0, 50.00)
#    motorControlL.setVelocity(0, 100.00)
#    motorControlR.setVelocity(0, 100.00)
#    sleep(5) #sleep for 5 seconds
#except PhidgetException as e:
#    print("Phidget Exception %i: %s" % (e.code, e.details))

#print("Step 2: Set acceleration to 100, decrease target speed to 75")
#try:
#    motorControlL.setAcceleration(0, 100.00)
#    motorControlL.setVelocity(0, 75.00)
#    sleep(5) #sleep for 5 seconds
#except PhidgetException as e:
#    print("Phidget Exception %i: %s" % (e.code, e.details))

#print("Step 3: Stop the motor by decreasing speed to 0 at 50 acceleration")
#try:
#    motorControlL.setAcceleration(0, 50.00)
#    motorControlL.setVelocity(0, 0.00)
#    sleep(5) #sleep for 5 seconds
#except PhidgetException as e:
#    print("Phidget Exception %i: %s" % (e.code, e.details))
#else:
#    try:
#        motorControlL.setAcceleration(0, 1.00)
#    except PhidgetException as e:
#        print("Phidget Exception %i: %s" % (e.code, e.details))

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    motorControlL.closePhidget()
    motorControlR.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)

