#!/usr/bin/env python
import time
import RPi.GPIO as GPIO

if __name__ == '__main__':
  print "hello world"

  GPIO.setmode(GPIO.BCM)

  GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  
  print "input 21 =",GPIO.input(21)
  
