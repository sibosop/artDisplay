
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

debug = True
currentSoundFile = ""

def setCurrentSound(file):
  global currentSoundFile
  soundTrack.eventMutex.acquire()
  currentSoundFile=file
  soundTrack.eventMutex.release()

class schlubTrack(threading.Thread):
  def run(self):
    global currentSoundFile
    syslog.syslog("Schlub Track")
    dir = adGlobal.eventDir
    while True:
      path=""
      nt = random.randint(soundTrack.eventMin,soundTrack.eventMax)/1000.0;
      try:
        file=""
        soundTrack.eventMutex.acquire()
        file = currentSoundFile
        soundTrack.eventMutex.release()
        if file == "":
          if debug: syslog.syslog("waiting for currentSoundFile");
          time.sleep(2)
          continue
        path = dir+"/"+file
        if debug: syslog.syslog("playing:"+path);
        sound = pygame.mixer.Sound(file=path)

        factor = ((soundTrack.speedChangeMax-soundTrack.speedChangeMin) 
                      * random.random()) + soundTrack.speedChangeMin
        nsound = soundTrack.speedx(sound,factor)
        if nsound is not None:
          sound = nsound
        l = random.random() * soundTrack.eventMaxVol
        r = random.random() * soundTrack.eventMaxVol
        soundTrack.playSound(sound,l,r)
      except Exception as e:
        syslog.syslog("error on "+path+":"+str(e))

      if debug: syslog.syslog("next play:"+str(nt))
      time.sleep(nt)
      if debug: syslog.syslog("back from sleep")

