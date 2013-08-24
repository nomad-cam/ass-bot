#!/usr/bin/env python
#

# Collect system variables and send to display and other ports


__author__ = 'Cameron Rodda'
__version__ = '0.0.1'
__date__ = '21 August 2013'

import commands
import zmq
import time


context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("ipc:///tmp/lcd.ipc")


def send_cat_msg(message, static, units='', line='1'):
    #msg = static.join(message)
    premsg = "%s: %s%s" % (static, message, units)
    #print( premsg )
    msg = {'message': premsg, 'line': line}
    zmq_socket.send_json(msg)
    time.sleep(3)


while True:

    #WLAN ip address
    wlan_ip = commands.getoutput("ip -f inet addr | grep wlan | tail -n 1 | awk '{print $2}' | cut -d '/' -f1")
    send_cat_msg(message=wlan_ip, static="wlan", line='0')

    #Memory
    memfree = commands.getoutput("cat /proc/meminfo | grep 'MemFree:' | awk '{ print $2 }'")
    send_cat_msg(str(memfree), "mfree", "KiB")
    memtotal =  commands.getoutput("cat /proc/meminfo | grep 'MemTotal:' | awk '{ print $2 }'")
    send_cat_msg(str(memtotal), "mtotal", "KiB")

    #System Load
    load1m = commands.getoutput(" w | grep 'load average' | awk '{print $(NF-2)}' | cut -d ',' -f1")
    send_cat_msg(str(load1m),"load1m")
    load5m = commands.getoutput(" w | grep 'load average' | awk '{print $(NF-1)}' | cut -d ',' -f1")
    send_cat_msg(str(load5m),"load5m")
    load15m = commands.getoutput(" w | grep 'load average' | awk '{print $(NF)}' | cut -d ',' -f1 ")
    send_cat_msg(str(load15m),"load15m")

    #Core utilisation
    coresum = commands.getoutput(" mpstat | tail -n 1 | awk '{print $4}' ")
    send_cat_msg(str(coresum),"coresum","%")
    core0usr = commands.getoutput(" mpstat -P 0 | tail -n 1 | awk '{print $4}' ")
    send_cat_msg(str(core0usr),"core0usr","%")
    core1usr = commands.getoutput(" mpstat -P 1 | tail -n 1 | awk '{print $4}' ")
    send_cat_msg(str(core1usr),"core1usr","%")
    core2usr = commands.getoutput(" mpstat -P 2 | tail -n 1 | awk '{print $4}' ")
    send_cat_msg(str(core2usr),"core2usr","%")
    core3usr = commands.getoutput(" mpstat -P 3 | tail -n 1 | awk '{print $4}' ")
    send_cat_msg(str(core3usr),"core3usr","%")

    #ETH0 ip address
    eth0_ip = commands.getoutput("ip -f inet addr | grep eth0 | tail -n 1 | awk '{print $2}' | cut -d '/' -f1")
    send_cat_msg(message=eth0_ip, static="eth0", line='0')

    #Core idle times
    coreidle = commands.getoutput(" mpstat | tail -n 1 | awk '{print $12}' ")
    send_cat_msg(str(coreidle),"coreidle","%")
    core0idle = commands.getoutput(" mpstat -P 0 | tail -n 1 | awk '{print $12}' ")
    send_cat_msg(str(core0idle),"core0idle","%")
    core1idle = commands.getoutput(" mpstat -P 1| tail -n 1 | awk '{print $12}' ")
    send_cat_msg(str(core1idle),"core1idle","%")
    core2idle = commands.getoutput(" mpstat -P 2| tail -n 1 | awk '{print $12}' ")
    send_cat_msg(str(core2idle),"core2idle","%")
    core3idle = commands.getoutput(" mpstat -P 3| tail -n 1 | awk '{print $12}' ")
    send_cat_msg(str(core3idle),"core3idle","%")

    #Wifi link data
    #wifi_essid = commands.getoutput("")
    wifi_wlan = commands.getoutput("cat /proc/net/wireless | tail -n 1 | awk '{print $1}' | cut -d ':' -f1")
    send_cat_msg(str(wifi_wlan),"device")
    wifi_link = commands.getoutput("cat /proc/net/wireless | tail -n 1 | awk '{print $3}' ")
    send_cat_msg(str(wifi_link),"link","0%")
    wifi_level = commands.getoutput("cat /proc/net/wireless | tail -n 1 | awk '{print $4}' ")
    send_cat_msg(str(wifi_level),"signal","0%")
    wifi_noise = commands.getoutput("cat /proc/net/wireless | tail -n 1 | awk '{print $5}' ")
    send_cat_msg(str(wifi_noise),"noise","0%")

    #Get a list of available wifi networks...
    #iwlist wlan10 scan | grep -e Quality -e ESSID -e Mode -e 'Signal level'
