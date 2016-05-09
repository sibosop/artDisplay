#!/usr/bin/env python
import serial
import os
import syslog
import adGlobal

def hasPanel():
  if os.path.exists(adGlobal.panelDev):
    syslog.syslog("Located usb serial device at "+adGlobal.panelDev)
    return True;
  syslog.syslog("No usb serial device at "+adGlobal.panelDev)
  return False;

def clear():
  ser.write([0xfe,0x51]) 
  
def setRow(r):
  val = 0 
  if ( r == 1 ):
    val = 0x40 
  ser.write([0xfe,0x45,val])

def printText(t):
    clear()
    ser.write('{0: ^15}'.format(t[0]))
    setRow(1)
    ser.write('{0: ^15}'.format(t[1]))
    
def setUpPanel():
  global ser
  if hasPanel():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    return True; 
  return False