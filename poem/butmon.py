#!/usr/bin/env python
import time
import platform
import syslog
import sys
import threading

debug=True


isRaspberry=platform.uname()[1] == 'raspberrypi';
if isRaspberry:
  if debug: 
    syslog.syslog("is raspberry")
  import RPi.GPIO as GPIO
else:
  if debug: syslog.syslog("is not raspberry");


class ButMonThread(threading.Thread):
  def __init__(self):
    super(ButMonThread,self).__init__()
    self.buts = {
      'blackBut' : { 'pin' : 5 , 'cb' : None }
      ,'redBut' : { 'pin' : 21 , 'cb' : None }
      ,'greenBut' : { 'pin' : 13, 'cb' : None  }
    }
    GPIO.setmode(GPIO.BCM)
    for k in self.buts.keys():
      GPIO.setup(self.buts[k]['pin'],GPIO.IN, pull_up_down=GPIO.PUD_UP)

  def run(self):
    while True:
      for k in self.buts.keys():
        if debug: syslog.syslog(k +":"+str(GPIO.input(self.buts[k]['pin'])))
        if GPIO.input(self.buts[k]['pin']):
          if debug: syslog.syslog(k +" is up")
        else:
          if debug: syslog.syslog(k +" is down")
          self.buts[k]['cb']()
      time.sleep(1)
      if debug:
        syslog.syslog(str(self.buts))
            
  def setCallback(self,but,cb):
    if but in self.buts.keys():
      self.buts[but]['cb'] = cb
    else:
      syslog.syslog(but+": not found for callback")
      
def testRed():
  syslog.syslog("testRed")
def testGreen():
  syslog.syslog("testGreen")
def testBlack():
  syslog.syslog("testBlack")

if __name__ == '__main__':
  test =  ButMonThread()
  test.setCallback("blackBut",testBlack)
  test.setCallback("greenBut",testGreen)
  test.setCallback("readBut",testRed)
  test.setDaemon(True)
  test.start()
  while True:
    time.sleep(1)
  
