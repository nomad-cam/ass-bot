#!/usr/bin/python 
###########################################################################################
# Filename:
#     CameraDriver.py
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
import Device as D
import Servo as S
import time

#################################
class CameraDriver(object):
    def __init__(self, trigger = False): # originally 0-4
        self.device = D.Device()
        self.servo_map = {}
        self.id_map = {}
        self.servo_list = []
        self.frame_list = []
        self.frame_list_length = 0
        self.frame_number = 0
        self.verbose = False
        self.trigger = trigger
        self.loop = False
        self.debug(self.device)
        self.device.go_home()

    def name_to_id(self, servo_name):
        return self.servo_map[servo_name].id

    def id_to_name(self, servo_id):
        return self.id_map[servo_id].label

    def load_file(self, filename = None):
        if not filename is None:
            try:
                if self.verbose:
                    print filename + "\n";
                self.servo_list, self.frame_list = self.read_config(filename)
                self.frame_list_length = len(self.frame_list)
            except (IndexError, IOError, EOFError):
                print "An error has occurred\n"
                self.unmount()
        else:    
            self.servo_list = [S.Servo(self.device, 'wrist'  , 0, 50, 50, 1200, 2000), \
                               S.Servo(self.device, 'camera' , 1, 0, 0, 992, 2000),\
                               S.Servo(self.device, 'elbow'  , 2, 6, 3, 1248, 2000),\
                               S.Servo(self.device, 'shoulder', 3, 6, 3, 992, 1888),\
                               S.Servo(self.device, 'base',     4, 4, 51, 992, 2000)]
        for servo in self.servo_list:
            self.servo_map[servo.label] = servo
            self.id_map[servo.id] = servo
        self.reset()
    
    def read_config(self, filename):
        if self.verbose:
            print "We are in config\n"
        frame_data = []
        current_frame_list = []
        output_servo_list = []
        with open(filename, 'r') as config:
            line = config.readline()
            while not ((line == '!end') or (line == '!END')):
                self.debug(line)
                datum = line.split()
                self.debug(datum)
                if len(datum) > 0:
                    if (datum[0] == '#'):
                        label = datum[1]
                        tag = int(datum[2])
                        temp_servo = S.Servo(self.device, label, tag, int(datum[3]), int(datum[4]), int(datum[5]), int(datum[6]))
                        output_servo_list.append(temp_servo)
                    if (datum[0] == '!'):
                        if self.trigger:
                            timer = 0
                        else:
                            timer = int(datum[6])
                        frame_data = [int(datum[1]), int(datum[2]), int(datum[3]), int(datum[4]), int(datum[5]), timer]
                        current_frame_list.append(frame_data)
                line = config.readline()    
        return output_servo_list, current_frame_list

    def status(self):
        return self.status_report()
    
    def status_report(self):
        output= ""
        for servo in self.servo_list:
            appended = servo.label + ": "+ str(servo.get_position())+"\t"
            output += appended
        output += "\n"
        return output
  
    def bounds(self):
        output = ""
        for servo in self.servo_list:
            appended = servo.label + ": "+ str(servo.bounds()) + "\t"
            output += appended
        output += "\n"
        return output

    def move(self, servo, dx):
        x = self.id_map[servo].get_position()
        x += dx
        self.id_map[servo].set_target(x)
    
    def goto_frame(self, position_list, wait_time=0):
        for servo_id in xrange(len(position_list)):
            temp_servo = self.id_map[servo_id]
            temp_servo.set_target(position_list[servo_id])
            self.debug((servo_id,position_list[servo_id]))
        time.sleep(wait_time)
        self.debug(wait_time)
    
    def reset(self):
        self.device.go_home()
        self.frame_number = 0
        self.frame_list_length = len(self.frame_list)

    def unmount(self):
        del(self.device)

    def import_frame_list(self, data):
        self.frame_list = data

    def step(self, report = False):
        return self.step_frame(report)

    def steps(self, N, report = False):
        responses = []
        for i in xrange(N):
            temp_report = self.step(report)
            responses.append(temp_report)
        return responses

    def step_frame(self, report = False):
        if 0 <= self.frame_number < self.frame_list_length:
            instruction = self.frame_list[self.frame_number]
            self.goto_frame(instruction[:-1], instruction[-1])
            self.debug(([self.frame_number, instruction]))
            if report:
                print([self.frame_number, instruction])
            self.frame_number += 1
            return True
        else:
            self.debug((self.frame_number,self.frame_list_length - 1))
            self.debug("Step out of bounds")
            return False

    def set_frame(self, frame_number):
        self.frame_number = frame_number
        self.debug(self.frame_number)

    def shift_frame(self, relative_frame_position):
        self.frame_number += relative_frame_position

    def execute_frame(self, target_frame_index):
        self.set_frame(target_frame_index)
        self.step()

    def execute_procedure(self, target_list):
        for target in target_list:
            self.execute_frame(target)
            print self.status()

    def debug(self, comment):
        if self.verbose:
            print comment
            print "\n"
