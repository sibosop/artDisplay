#!/usr/bin/env python
import serial
import time


def clear():
  ser.write([0xfe,0x51]) 
  
def setRow(r):
  val = 0 
  if ( r == 1 ):
    val = 0x40 
  ser.write([0xfe,0x45,val])
  
  
if __name__ == '__main__':
  print "hello world"
  ser = serial.Serial('/dev/tty.usbserial-AM01VG98', 9600)
  while True:
    clear();
    setRow(0)
    ser.write("fuck bubble")
    setRow(1)
    ser.write('b')
    time.sleep(2)