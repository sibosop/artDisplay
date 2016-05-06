#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import syslog

def isMaster():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  if GPIO.input(21):
    syslog.syslog("is not master");
    return False;
  syslog.syslog("is master")
  return True;
  
if __name__ == '__main__':
  isMaster()

