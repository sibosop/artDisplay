#!/usr/bin/env python

import threading
import time
import syslog
import subprocess
import glob
import adGlobal
import sys
import random
import urllib
import soundFile
import slp


debug = True
enabled = True

playerMutex=threading.Lock()

def enable(val):
  global enabled
  playerMutex.acquire()
  enabled = val
  playerMutex.release()
  if debug: syslog.syslog("player enabled:"+str(enabled))

def isEnabled():
  global enabled
  playerMutex.acquire()
  rval = enabled
  playerMutex.release()
  return rval

class playerThread(threading.Thread):
  def run(self):
    edir = adGlobal.eventDir
    first = True
    while True:
      try:
        if isEnabled() is False:
          if first:
            first = False
            if debug: syslog.syslog("PLAYER: DISABLING AUTO PLAYER")
          time.sleep(2)
          continue
        first = True
        hosts = slp.getHosts("schlub")
        e = soundFile.getSoundEntry()
        choice = e.name
        if debug: syslog.syslog("player choosing "+choice)
        for h in hosts:
          ip = h['ip']
          if debug: syslog.syslog("sending request to "+ip)
          request = "http://"+ip+":8080/player?play="+choice
          if debug: syslog.syslog("request;"+request)
          f = urllib.urlopen(request)
          test = f.read()
          if debug: syslog.syslog("got response:"+test)
        stime = random.randint(15,40)
        if debug: syslog.syslog("next change:"+str(stime))
        time.sleep(stime)
      except Exception, e:
        syslog.syslog("player error: "+repr(e))
