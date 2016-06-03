#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import syslog
import sys

def isMaster():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  if GPIO.input(21):
    sys.stderr.write("is not master"+"\n");
    return False;
  sys.stderr.write("is master"+"\n")
  return True;
  
if __name__ == '__main__':
  isMaster()

