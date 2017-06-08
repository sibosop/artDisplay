#!/usr/bin/env python
import time
import platform
import syslog
import sys

debug=False
isRaspberry=platform.uname()[1] == 'raspberrypi';
if isRaspberry:
	import RPi.GPIO as GPIO


def isMaster():
  if isRaspberry:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(21):
      syslog.syslog("is not master");
      return False;

  syslog.syslog("is master")
  return True;

def isDispText():
  if isRaspberry:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(13):
      syslog.syslog("is not disp text");
      return False;

  syslog.syslog("is disp text")
  return True;

def hasAudio():
  if isRaspberry:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(5):
      if debug: syslog.syslog("no audio");
      return False;
  if debug: syslog.syslog("has audio")
  return True;
  
if __name__ == '__main__':
  isMaster()
  isDispText()
  hasAudio()

