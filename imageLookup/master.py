#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import syslog
import sys

def isMaster():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  if GPIO.input(21):
    syslog.syslog("is not master");
    return False;
  syslog.syslog("is master")
  return True;

def isDispText():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  if GPIO.input(13):
    syslog.syslog("is not disp text");
    return False;
  syslog.syslog("is disp text")
  return True;
  
if __name__ == '__main__':
  isMaster()
  isDispText()

