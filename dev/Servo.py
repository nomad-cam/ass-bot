#!/usr/bin/python 
###########################################################################################
# Filename: 
#     Servo.py
###########################################################################################
# Project Authors: 
#     Juhapekka Piiroinen
#     Brian Wu
# 
# Changes:
#     June 14, 2010 by Juhapekka Piiroinen - changes committed to svn
#           - added comments for the device commands according to the manual from Pololu
#           - added latest draft code for rotating base servo (Parallax Continuous Rotating Servo)
#           - note! you should be able to clear error flags with .get_errors function according to the manual
#           - renamed CameraDriver to LegacyCameraDriver as Brian Wu has done better one
#           - integrated batch of changes provided by Brian Wu
#
#     June 11, 2010 by Brian Wu - Changes committed thru email
#           - Decoupling the implementation from the program
#
#     April 19, 2010 by Juhapekka Piiroinen
#           - Initial Release
# 
# Email:
#     juhapekka.piiroinen@gmail.com
#
# License: 
#     GNU/GPLv3
#
# Description:
#     A python-wrapper for Pololu Micro Maestro 6-Channel USB Servo Controller
#
############################################################################################
# /!\ Notes /!\
# You will have to enable _USB Dual Port_ mode from the _Pololu Maestro Control Center_.
#
############################################################################################
# Device Documentation is available @ http://www.pololu.com/docs/pdf/0J40/maestro.pdf
############################################################################################
# (C) 2010 Juhapekka Piiroinen
#          Brian Wu
############################################################################################
class Servo(object):
	def __init__(self, driver, label = 'Servo', id_num = 0, speed=0, accel=0, low_pos=700, high_pos = 2100):
		self.driver = driver
		self.label = label
		self.id = id_num
		self.speed = speed
		self.accel = accel
		if high_pos < low_pos:
			raise ValueError("Bounds of Servo do not make sense %s !< %s" % (low_pos, high_pos))  
		self.low_pos = low_pos
		self.high_pos = high_pos
		
		self.driver.set_acceleration(self.id, self.accel)
		self.driver.set_speed(self.id, self.speed)

	def bounds(self):
		return (self.low_pos, self.high_pos)
	def get_position(self):
		return self.driver.get_position(self.id)
	def fit_bound(self, value):
		return max( min(self.high_pos, value), self.low_pos)
	def set_target(self, value):
		self.driver.set_target(self.id, self.fit_bound(value))
