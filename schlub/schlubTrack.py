#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import soundTrack
import threading
import adGlobal
import pygame
import syslog
import random
import time
import soundServer

debug = True
currentSoundFile = ""
soundMaxVol = 1.0
soundMinVol = 0.1

def setSoundMaxVolume(vol):
  global soundMaxVol
  soundMaxVol = vol
  

def findSoundFile(file):
  dir = adGlobal.eventDir
  path = dir+"/"+file
  rval = ""
  if os.path.isfile(path):
    rval = path
  return rval

def setCurrentSound(file):
  global currentSoundFile
  rval = "fail"
  if findSoundFile(file) != "":
    soundTrack.eventMutex.acquire()
    currentSoundFile=file
    soundTrack.eventMutex.release()
    rval = "ok"
  return soundServer.jsonStatus(rval)

def getCurrentSound():
  global currentSoundFile
  soundTrack.eventMutex.acquire()
  rval = currentSoundFile
  soundTrack.eventMutex.release()
  n = currentSoundFile.rfind(".")
  return rval[0:n]

def doJpent():
  rval = ((soundTrack.speedChangeMax-soundTrack.speedChangeMin) 
                        * random.random()) + soundTrack.speedChangeMin
  syslog.syslog("doJpent")
  return rval

tunings = {
  'jpent' : [1.0,32.0/27.0,4.0/3.0,3.0/2.0,16.0/9.0]
}

octaves = [0.25,0.5,1.0,2.0,4.0]

def getFactor(path):
  rval = 1.0
  try:
    pos = path.find("__");
    if pos == -1:
      raise NameError
    epos = path.find(".",pos)
    if pos == -1:
      raise NameError

    tuning = path[pos+2:epos]
    syslog.syslog("tuning:"+tuning);
    if tuning not in tunings:
      syslog.syslog("bad tuning:"+tuning)
      raise NameError
    rval = random.choice(tunings[tuning]) * random.choice(octaves)
  except NameError as exp:
    syslog.syslog("default tuning for path:"+path)
    rval = ((soundTrack.speedChangeMax-soundTrack.speedChangeMin) 
                      * random.random()) + soundTrack.speedChangeMin
  syslog.syslog("factor:"+str(rval))
  return rval


class schlubTrack(threading.Thread):
  def __init__(self,name):
    super(schlubTrack,self).__init__()
    self.runState = True
    self.name = name
    self.runMutex = threading.Lock()


  def isRunning(self):
    self.runMutex.acquire()
    rval = self.runState
    self.runMutex.release()
    return rval

  def stop(self):
    self.runMutex.acquire()
    self.runState = False
    self.runMutex.release()
    
  def run(self):
    global currentSoundFile
    syslog.syslog("Schlub Track:"+self.name)
    dir = adGlobal.eventDir
    while self.isRunning():
      path=""
      nt = random.randint(soundTrack.eventMin,soundTrack.eventMax)/1000.0;
      try:
        file=""
        soundTrack.eventMutex.acquire()
        file = currentSoundFile
        soundTrack.eventMutex.release()
        if file == "":
          if debug: syslog.syslog(self.name+": waiting for currentSoundFile");
          time.sleep(2)
          continue
        path = dir+"/"+file
        if debug: syslog.syslog(self.name+": playing:"+path);
        sound = pygame.mixer.Sound(file=path)
	
        factor = getFactor(path);
        nsound = soundTrack.speedx(sound,factor)
        if nsound is not None:
          sound = nsound
        l = random.uniform(soundMinVol,soundMaxVol);
        r = l
        soundTrack.playSound(sound,l,r)
      except Exception as e:
        syslog.syslog(self.name+": error on "+path+":"+str(e))

      if debug: syslog.syslog(self.name+": next play:"+str(nt))
      time.sleep(nt)
      if debug: syslog.syslog(self.name+":back from sleep")
    syslog.syslog("schlub thread " + self.name + " exiting")

ecount = 0
eventThreads=[]
def startEventThread():
  if debug: syslog.syslog("startEventThread")
  global eventThreads
  global ecount
  ecount += 1
  t=schlubTrack(str(ecount))
  eventThreads.append(t)
  eventThreads[-1].setDaemon(True)
  eventThreads[-1].start()

def stopEventThread():
  global eventThreads
  if debug: syslog.syslog("stopEventThread")
  if len(eventThreads) != 0:
    t = eventThreads.pop()
    t.stop()
  else:
    syslog.syslog("trying to stop thread when list is empty")



def changeNumSchlubThreads(n):
  global eventThreads
  syslog.syslog("changing number of threads from "
                    +str(len(eventThreads))+ " to "+str(n))
  while len(eventThreads) != n:
    if len(eventThreads) < n:
      startEventThread()
    elif len(eventThreads) > n:
      stopEventThread()
  return soundServer.jsonStatus("ok")
