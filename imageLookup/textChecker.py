#!/usr/bin/env python
import os
import time
import serial
debug = False
def clear():
  ser.write([0xfe,0x51]) 
  
def setRow(r):
  val = 0 
  if ( r == 1 ):
    val = 0x40 
  ser.write([0xfe,0x45,val])

def printText(t):
    clear()
    ser.write(t[0])
    setRow(1)
    ser.write(t[1])
      
textExt = ".lkp"
def getText():
  filenames = next(os.walk(cacheDir))[2]
  for f in filenames:
    if debug:
      print "filename:",f
    try:
      ext = f.rindex(textExt)
    except ValueError:
      if debug:
        print "not lookup text file"
      continue
    flag = f[ext:]
    if flag == textExt:  
      if debug:
        print "found text file",f
      path = cacheDir + "/" + f
      lines = open(path).read().split('\n')
      if len(lines) > 1:
        os.unlink(path)
        return lines
      
  return None
  
if __name__ == '__main__':
  ser = serial.Serial('/dev/ttyUSB0', 9600)
  cacheDir = os.environ.get('ID_CACHE');
  if cacheDir is None:
    print "Error: ID_CACHE not defined"
    exit(-1)
  if debug:  
    print "image cache dir:",cacheDir
  if not os.path.exists(cacheDir):
    print "Error: chacheDir",cacheDir,"does not exist"
    exit(-1)
  count=0
  while True:
    if debug:
      count += 1
      print "checking for text. count:",count
    text = getText();
    if text == None:
      if debug:
        print "no text"
    else:
      if debug:
        print "found test",text
      printText(text)
    time.sleep(5)