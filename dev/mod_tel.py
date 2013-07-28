#!/usr/bin/env python
#

#functions for box stats
import psutil
import commands

#zeromq libs
import zmq

from time import sleep
#open the zmq ports (:8888 for telemetry comms)
context = zmq.Context()

sock_ipc = context.socket(zmq.REQ)
#subscribe.connect('ipc://telemetry.ipc')
#subscribe to all traffic on this port...
#subscribe.setsockopt(zmq.SUBSCRIBE,"telemetry")

#context1 = zmq.Context()
publish = context.socket(zmq.PUB)
publish.connect('tcp://*:8865')

poller = zmq.Poller()
poller.register(sock_ipc, zmq.POLLIN)

def collectStats(stats_req):
    statsdict = {}
    
    for stats in stats_req:
        print "Fetching: %s" % stats
        sock_ipc.connect('ipc://telemetry/%s.ipc' % stats)
        try:
            sock_ipc.send( 'True' , zmq.NOBLOCK )
        except:
            #if unable to send assume worst and continue
            statsdict[stats] = 'NaN'
            pass

        #timeout after 500ms - doesn't need to be much faster
        socks = dict(poller.poll(500))
        if socks:
            if socks.get(sock_ipc) == zmq.POLLIN:
                #msg = sock_ipc.recv(zmq.NOBLOCK)
                statsdict[stats] = sock_ipc.recv(zmq.NOBLOCK)
        else:
            #if no resonse given assume worst and continue
            statsdict[stats] = 'NaN'
            print "Error: message receive timeout"

#        print 'Closing sock_ipc?'
#        sock_ipc.close()
#        sleep(1.)

    return statsdict


def readBatStat():
#    pass    
    rem = float(commands.getoutput("grep \"^remaining capacity\" /proc/acpi/battery/BAT0/state | awk '{ print $3 }'"))
    full = float(commands.getoutput("grep \"^last full capacity\" /proc/acpi/battery/BAT0/info | awk '{ print $4 }'"))
    state = commands.getoutput("grep \"^charging state\" /proc/acpi/battery/BAT0/state | awk '{ print $3 }'")
 
    perc = int((rem/full) * 100)

    return rem,full,state,perc


def readWifiStat():
#    pass
    chan = commands.getoutput('iwlist wlan0 channel')
    txpow = commands.getoutput('iwlist wlan0 txpower')
    wap = commands.getoutput('iwlist wlan0 accesspoints')
    freq = commands.getoutput('iwlist wlan0 frequency')
    rate = commands.getoutput('iwlist wlan0 rate')

    return chan,freq,txpow,wap,rate


stats_req = ['mod_com','mod_mot','mod_sen','mod_cam','mod_aut']

while True:
#    subscribers = dict(poller.poll(200))
#    if subscribers:
#        if subscribers.get(subscribe) == zmq.POLLIN:
#            msg = subscribe.recv(zmq.NOBLOCK)
#            print "Got message: ", msg
#    else:
#        print "Error: messgae receive timeout"
#    stats_req = ['mod_com','mod_mot','mod_sen','mod_cam','mod_aut']
#
    tel = collectStats(stats_req)
   
    cpu_load = psutil.cpu_percent()
    mem_load = psutil.virtual_memory()
    batstat = readBatStat()
    print batstat[2]

    tel['mod_tel'] = ['OK',cpu_load,mem_load[1],mem_load[2],batstat[2],batstat[3]]
#    print cpu_load,mem_load[2],tel,repr(tel)

    try:
        publish.send(repr(tel),zmq.NOBLOCK)
    except:
        pass
    #Send all data back to central command...
    #publish.send()
