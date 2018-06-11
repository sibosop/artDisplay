#!/usr/bin/env python

import threading
import time
import subprocess
import glob
import random
import json
import os
import sys
import gardenSoundFile

debug = True
enabled = True

playerMutex=threading.Lock()

def enable(val):
  global enabled
  playerMutex.acquire()
  enabled = val
  playerMutex.release()
  if debug: print("player enabled:"+str(enabled))

def isEnabled():
  global enabled
  playerMutex.acquire()
  rval = enabled
  playerMutex.release()
  return rval

class playerThread(threading.Thread):
  def __init__(self,tList):
    super(playerThread,self).__init__()
    self.tList = tList
    self.done = False
    
  def run(self):
    while gardenSoundFile.testBumpCollection():
      try:
        e = gardenSoundFile.getSoundEntry()
        if debug: print("player choosing "+str(e))
        for t in self.tList:
          choice = random.choice(e)
          if debug: print("sending "+choice+" request to "+t.name)
          t.setCurrentSound({'file' : choice})
        stime = random.randint(15,40)
        if debug: print("next change:"+str(stime))
        time.sleep(stime)
      except Exception, e:
        print("player error: "+repr(e))
        os._exit(3)
    for t in self.tList:
      t.stop()
    self.done = True
