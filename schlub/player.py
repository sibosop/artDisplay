#!/usr/bin/env python

import threading
import time
import syslog
import subprocess
import glob
import adGlobal
import sys
import random
import urllib2
import soundFile
import slp
import json
import schlubTrack


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
        if debug: syslog.syslog("player choosing "+str(e))
        for h in hosts:
          choice = random.choice(e)
          ip = h['ip']
          if adGlobal.isLocalHost(ip):
            if debug: syslog.syslog("sending "+choice+" request to localhost("+ip+")")
            schlubTrack.setCurrentSound(choice)
          else:
            if debug: syslog.syslog("sending "+choice+" request to "+ip)
            url = "http://"+ip+":8080"
            if debug: syslog.syslog("url:"+url)
            cmd = { 'cmd' : "Sound" , 'args' : [choice] }
            req = urllib2.Request(url
                      ,json.dumps(cmd),{'Content-Type': 'application/json'})
            f = urllib2.urlopen(req)
            test = f.read()
            if debug: syslog.syslog("got response:"+test)
        stime = random.randint(15,40)
        if debug: syslog.syslog("next change:"+str(stime))
        time.sleep(stime)
      except Exception, e:
        syslog.syslog("player error: "+repr(e))
