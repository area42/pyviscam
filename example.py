#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from pyviscam.broadcast import Viscam, Camera

print '----- visca bus initialisation -----'
# create a visca bus object
cams = Viscam()
# get a list of serial ports available and select the last one
ports = cams.serial.listports()
port = None
for item in ports:
	if 'usbserial' in item:
		port = item
if not port:
	port = ports[0]
print('serial port opening : ' + port)
# open a connection on the serial object
cams.reset(port)
v1 = cams.get_instances()[0]

print v1.getters()
print v1.setters()
print v1.describe('iris')

# print('available parameters : ')
# print('-------------------------')
# prop_list = [p for p in dir(Camera) if isinstance(getattr(Camera, p),property)]
# print sorted(prop_list,cmp=lambda x,y: cmp(x.lower(), y.lower()))
#v1.WB_mode = 'bla'

v1.AE_mode = 'auto'
# v1.iris    = 0
# sleep(10)
# v1.Iris	   = 40
v1.WB_mode	   = 'table'
v1.WB_table    = 25
# print v1.backlight
# v1.backlight = 'on'
# print v1.backlight
# v1.backlight = 'off'
# print v1.backlight

# v1.WB_mode='table'
# print v1.WB_table
# v1.WB_table = 25
# print v1.WB_table
