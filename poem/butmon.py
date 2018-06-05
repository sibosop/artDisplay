#!/usr/bin/env python
import time
import poem
import platform
import syslog
import sys
import threading
import os
home = os.environ['HOME']
if poem.useVoice:
  sys.path.append(home+"/GitProjects/artDisplay/shared")
  import asoundConfig

debug=True


isRaspberry=platform.uname()[1] == 'raspberrypi';
if isRaspberry:
  if debug: 
    syslog.syslog("is raspberry")
  import RPi.GPIO as GPIO
else:
  if debug: syslog.syslog("is not raspberry");


class ButMonThread(threading.Thread):
  def testRed(self):
    self.currentVol += 1
    if self.currentVol > 100:
      self.currentVol = 100
      return
    asoundConfig.setVolume(self.currentVol)

  def testGreen(self):
    if self.currentVol == 0:
      return;
    self.currentVol -= 1
    asoundConfig.setVolume(self.currentVol)

  def testBlack(self):
    syslog.syslog("testBlack")
    os._exit(2)

  def __init__(self):
    super(ButMonThread,self).__init__()
    self.buts = {
      'blackBut' : { 'pin' : 21 , 'cb' : None }
      ,'redBut' : { 'pin' : 5 , 'cb' : None }
      ,'greenBut' : { 'pin' : 13, 'cb' : None  }
    }
    GPIO.setmode(GPIO.BCM)
    for k in self.buts.keys():
      GPIO.setup(self.buts[k]['pin'],GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if poem.useVoice:
      self.currentVol = asoundConfig.getVolume()
      self.setCallback("greenBut",self.testGreen)
      self.setCallback("redBut",self.testRed)
    self.setCallback("blackBut",self.testBlack)


  def run(self):
    while True:
      for k in self.buts.keys():
        #if debug: syslog.syslog(k +":"+str(GPIO.input(self.buts[k]['pin'])))
        if GPIO.input(self.buts[k]['pin']) == 0:
          self.buts[k]['cb']()
      time.sleep(.1)
     # if debug: syslog.syslog(str(self.buts))
            
  def setCallback(self,but,cb):
    if but in self.buts.keys():
      self.buts[but]['cb'] = cb
    else:
      syslog.syslog(but+": not found for callback")
      


if __name__ == '__main__':
  test =  ButMonThread()
  test.setDaemon(True)
  test.start()
  while True:
    time.sleep(1)
  
