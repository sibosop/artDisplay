#!/usr/bin/env python
import pygame
import os


eventMin=100
eventMax=10000
debug=True

def setup():
  pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
  pygame.init()

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
  
  
class schlubTrack(threading.Thread):
  def __init__(self,name,dir):
    super(schlubTrack,self).__init__()
    self.runState = True
    self.name = name
    self.currentSound={'file' : ""}
    self.currentDir = 
    self.soundDir= os.getcwd()
    self.soundMutex = threading.Lock()
    self.runMutex = threading.Lock()
    self.dirMutex = threading,Lock()
    
  def setCurrentDir(self,dir):
    self.dirMutex.acquire()
    self.soundDir = dir
    self.dirMutex.release()
  
  def getCurrentDir(self,dir):
    self.dirMutex.acquire()
    dir = self.soundDir
    self.dirMutex.release()
    return dir
    
  def setCurrentSound(self,cs):
    self.soundMutex.acquire()
    self.currentSound = cs
    self.soundMutex.release()
  
  def getCurrentSound(self,cs):
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
        path = self.getCurrentDir()+"/"+file
        if debug: print(self.name+": playing:"+path);
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

      if debug: print(self.name+": next play:"+str(nt))
      time.sleep(nt)
      if debug: print(self.name+":back from sleep")
    print("schlub thread " + self.name + " exiting")
    
ecount = 0
eventThreads=[]
def startGardenThread():
  if debug: syslog.syslog("startGardenThread")
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
  syslog.syslog("changing number of threads from "
                    +str(len(eventThreads))+ " to "+str(n))
  while len(eventThreads) != n:
    if len(eventThreads) < n:
      startEventThread()
    elif len(eventThreads) > n:
      stopEventThread()
  return True

  