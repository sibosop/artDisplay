
#!/usr/bin/env python
import serial
import os
import syslog
import adGlobal
debug=True
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
    if debug: print "len:",t[0],len(t[0])
    ser.write('{0: ^16}'.format(t[0]).upper())
    if debug: print "len:",t[1],len(t[1])
    setRow(1)
    ser.write('{0: ^16}'.format(t[1]).upper())
    
def setUpPanel():
  global ser
  if hasPanel():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    return True; 
  return False
