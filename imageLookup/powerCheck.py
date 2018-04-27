#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import syslog
import subprocess
import threading
import adGlobal
import RPi.GPIO as GPIO
import time
import slp

def doShutdown():
  syslog.syslog("doing shutdown");
  hosts = slp.getHosts("artDisplay")
  for h in hosts:
    if adGlobal.isLocalHost(h['ip']):
      syslog.syslog("skipping localhost shutdown")
    else:
      try:
        syslog.syslog("calling shutdown for:"+ h['ip'])
        subprocess.check_output(["ssh","pi@"+h['ip'],"sudo","poweroff"])
      except:
        syslog.syslog("ignoring shutdown error")
  syslog.syslog("shutting down");
  subprocess.check_output(["sudo","poweroff"])

if __name__ == '__main__':
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  while True:
    if GPIO.input(16) :
      time.sleep(1)
      continue
    doShutdown()

