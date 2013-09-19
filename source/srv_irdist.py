#!/usr/bin/env python
#

import time
import sys
import zmq

#Basic imports
from ctypes import *
#import sys
import random
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

#Create an interfacekit object
try:
    interfaceKitHUB = InterfaceKit()
    interfaceKitLCD = InterfaceKit()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKitHUB.isAttached(), interfaceKitHUB.getDeviceName(), interfaceKitHUB.getSerialNum(), interfaceKitHUB.getDeviceVersion()))
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKitLCD.isAttached(), interfaceKitLCD.getDeviceName(), interfaceKitLCD.getSerialNum(), interfaceKitLCD.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKitHUB.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKitHUB.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKitHUB.getSensorCount()))

#Event Handler Callback Functions
def interfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))

def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))

def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def interfaceKitInputChanged(e):
    source = e.device
    print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

def interfaceKitSensorChanged(e):
    source = e.device
    print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))

def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

#Main Program Code
try:
    interfaceKitHUB.setOnAttachHandler(interfaceKitAttached)
    interfaceKitHUB.setOnDetachHandler(interfaceKitDetached)
    interfaceKitHUB.setOnErrorhandler(interfaceKitError)
    interfaceKitHUB.setOnInputChangeHandler(interfaceKitInputChanged)
    interfaceKitHUB.setOnOutputChangeHandler(interfaceKitOutputChanged)
    interfaceKitHUB.setOnSensorChangeHandler(interfaceKitSensorChanged)

    interfaceKitLCD.setOnAttachHandler(interfaceKitAttached)
    interfaceKitLCD.setOnDetachHandler(interfaceKitDetached)
    interfaceKitLCD.setOnErrorhandler(interfaceKitError)
    interfaceKitLCD.setOnInputChangeHandler(interfaceKitInputChanged)
    interfaceKitLCD.setOnOutputChangeHandler(interfaceKitOutputChanged)
    interfaceKitLCD.setOnSensorChangeHandler(interfaceKitSensorChanged)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
# Open interfaceKit by serial number to avoid conflicts with future interface kits...
# As displayed by displayDeviceInfo()
    interfaceKitLCD.openPhidget(serial=120517)
    interfaceKitHUB.openPhidget(serial=337662)
    
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    interfaceKitHUB.waitForAttach(10000)
    interfaceKitLCD.waitForAttach(10000)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKitHUB.closePhidget()
        interfaceKitLCD.closePhidget()
        
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Setting the data rate for each sensor index to 4ms....")
for i in range(interfaceKitHUB.getSensorCount()):
    try:

        interfaceKitHUB.setDataRate(i, 4)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

print "\n"
#print out the array distance...
#seems to be accurate to around +/-2mm
for i in range(interfaceKitHUB.getSensorCount()):
    try:
        intval = interfaceKitHUB.getSensorValue(i)
        if not intval:
            continue
        distance_mm = (9462/(intval - 16.92)) * 10

        #Not a reliable mesaurement below 200mm (20cm) or above 1500 (150cm)
        if (distance_mm < 200.0) or (distance_mm > 1500.0):
            distance_mm = "NaN"

        print( distance_mm )
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

print "Sensor ValueHUB",interfaceKitHUB.getSensorValue(0)
print "Sensor ValueLCD",interfaceKitLCD.getSensorValue(0)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKitHUB.closePhidget()
    interfaceKitLCD.closePhidget()

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)

