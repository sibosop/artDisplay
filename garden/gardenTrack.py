#!/usr/bin/env python
import pygame
import os
import threading
import random
import time
import numpy as np

debug = True
currentSound = {'file':""}
soundMaxVol = 1.0
soundMinVol = 0.1
speedChangeMax = 4.0
speedChangeMin = .25
eventMin=100
eventMax=10000
debug=True

def setup():
  pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
  pygame.init()
  
def speedx(sound, factor):
  rval = None
  try:
    print("speedx factor:"+str(factor))
    sound_array = pygame.sndarray.array(sound)
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    rval = pygame.sndarray.make_sound(sound_array[ indices.astype(int) ])
  except Exception as e:
    print("speedx:"+str(e))
  return rval

def playSound(sound,l,r):
  eventChan = None
  eventChan=pygame.mixer.find_channel()
  if eventChan is None:
    pygame.mixer.set_num_channels(pygame.mixer.get_num_channels()+1);
    eventChan=pygame.mixer.find_channel()
  print("busy channels:"+str(getBusyChannels()))
  print("l: "+str(l) + " r:"+str(r))
  eventChan.set_volume(l,r)
  eventChan.play(sound)
  eventChan.set_endevent()
  
def getBusyChannels():
  count = 0
  for i in range(pygame.mixer.get_num_channels()):
    if pygame.mixer.Channel(i).get_busy():
      count +=1
  return count

def playFile(path):
  print "playing",path
  sound = pygame.mixer.Sound(file=path)
  playSound(sound,.5,.5)

def doJpent():
  rval = ((speedChangeMax-speedChangeMin) 
                        * random.random()) + speedChangeMin
  print("doJpent")
  return rval

tunings = {
  'jpent' : [1.0,32.0/27.0,4.0/3.0,3.0/2.0,16.0/9.0]
  ,'bfarabi' : [1.0,9.0/8.0,45.0/32.0,131.0/90.0,3.0/2.0,15.0/8.0,31.0/16.0]
  ,'sheng' : [1.0,8.0/7.0,6.0/5.0,5.0/4.0,3.0/2.0,5.0/3.0]
  ,'joy' : [1.0,9.0/8.0,5.0/4.0,3.0/2.0,5.0/3.0,15.0/8.0]
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
    print("tuning:"+tuning);
    if tuning not in tunings:
      print("bad tuning:"+tuning)
      raise NameError
    rval = random.choice(tunings[tuning]) * random.choice(octaves)
  except NameError as exp:
    print("default tuning for path:"+path)
    rval = ((speedChangeMax-speedChangeMin) * random.random()) + speedChangeMin
  print("factor:"+str(rval))
  return rval
  
  
class gardenTrack(threading.Thread):
  def __init__(self,name):
    super(gardenTrack,self).__init__()
    self.runState = True
    self.name = name
    self.currentSound={'file' : ""}
    self.currentDir = os.getcwd()
    
    self.soundMutex = threading.Lock()
    self.runMutex = threading.Lock()
    self.dirMutex = threading.Lock()
    
  def setCurrentDir(self,dir):
    self.dirMutex.acquire()
    self.soundDir = dir
    self.dirMutex.release()
  
  def getCurrentDir(self):
    self.dirMutex.acquire()
    dir = self.soundDir
    self.dirMutex.release()
    return dir
    
  def setCurrentSound(self,cs):
    self.soundMutex.acquire()
    self.currentSound = cs
    self.soundMutex.release()
  
  def getCurrentSound(self):
    self.soundMutex.acquire()
    cs = self.currentSound 
    self.soundMutex.release()
    return cs
    
 
  
    
  def isRunning(self):
    self.runMutex.acquire()
    rval = self.runState
    self.runMutex.release()
    return rval

  def stop(self):
    self.runMutex.acquire()
    self.runState = False
    self.runMutex.release()
    return rval
    
  def run(self):
    print("Garden Track:"+self.name)
    while self.isRunning():
      path=""
      nt = random.randint(eventMin,eventMax)/1000.0;
      try:
        cs = self.getCurrentSound()
        file=""
        file = cs['file']
        if file == "":
          if debug: print(self.name+": waiting for currentSoundFile");
          time.sleep(2)
          continue
        path = self.getCurrentDir()+file
        #path = "/Users/brian/sibosopLocal/music/Music20161008/Clips/schlubFull/a1.wav"
        if debug: print(self.name+": playing:"+path);
        sound = pygame.mixer.Sound(file=path)

        factor = getFactor(path);
        nsound = speedx(sound,factor)
        if nsound is not None:
          sound = nsound
        l = random.uniform(soundMinVol,soundMaxVol);
        r = l
        playSound(sound,l,r)
      except Exception as e:
        print(self.name+": error on "+path+":"+str(e))

      if debug: print(self.name+": next play:"+str(nt))
      time.sleep(nt)
      if debug: print(self.name+":back from sleep")
    print("schlub thread " + self.name + " exiting")
    
ecount = 0
eventThreads=[]
def startEventThread():
  if debug: print("startEventThread")
  global eventThreads
  global ecount
  ecount += 1
  t=gardenTrack(str(ecount))
  eventThreads.append(t)
  eventThreads[-1].setDaemon(True)
  eventThreads[-1].start()

def stopEventThread():
  global eventThreads
  if debug: print("stopEventThread")
  if len(eventThreads) != 0:
    t = eventThreads.pop()
    t.stop()
  else:
    print("trying to stop thread when list is empty")


def changeNumGardenThreads(n):
  global eventThreads
  print("changing number of threads from "
                    +str(len(eventThreads))+ " to "+str(n))
  while len(eventThreads) != n:
    if len(eventThreads) < n:
      startEventThread()
    elif len(eventThreads) > n:
      stopEventThread()
  return True

  