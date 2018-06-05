#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import soundTrack
import threading
import adGlobal
import pygame
import textSpeaker
import syslog
import time
import random
import soundServer
import schlubTrack

phraseScatter = False;
currentPhrase=""
phraseMutex=threading.Lock()
debug=True
phraseMinVol = 0.7
phraseMaxVol = 1.0

def setPhraseScatter(flag):
  global phraseScatter
  phraseScatter = (flag == "true")
  return soundServer.jsonStatus("ok")


def setCurrentPhrase(args):
  global currentPhrase
  phraseMutex.acquire()
  currentPhrase=args['phrase']
  phraseMutex.release()
  syslog.syslog("current phrase:"+currentPhrase)
  if currentPhrase == "":
    if debug: syslog.syslog("set sound max volume to 1.0")
    schlubTrack.setSoundMaxVolume(1.0)
  else:
    if debug: syslog.syslog("set sound max volume to 0.5")
    schlubTrack.setSoundMaxVolume(0.5)
  return soundServer.jsonStatus("ok")

def getCurrentPhrase():
  global currentPhrase
  phraseMutex.acquire()
  rval = currentPhrase
  phraseMutex.release()
  return rval


class schlubSpeakThread(threading.Thread):
  def __init__(self):
    super(schlubSpeakThread,self).__init__()
    self.runState = True
    self.runMutex = threading.Lock()
    self.name = "schlubSpeak"

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
    global currentPhrase
    global phraseScatter
    if debug: syslog.syslog(self.name+": starting")
    dir = adGlobal.eventDir
    oldPhrase = ""
    sound = None
    while self.isRunning():
      try:
        phrase = getCurrentPhrase();
        if phrase == "":
          time.sleep(1)
          continue
        if phrase == "--":
          setCurrentPhrase("");
          time.sleep(1)
          continue
        phrase = phrase.replace("-"," ")
        if debug: syslog.syslog("PhraseScatter:"+str(phraseScatter))
        if phraseScatter:
          phrase = random.choice(phrase.split())
        if oldPhrase != phrase:
          oldPhrase = phrase
          path = textSpeaker.makeSpeakFile(phrase)
          if path is None:
            syslog.syslog("conversion of "+phrase+" failed")
            time.sleep(1)
            continue
          if debug: syslog.syslog(self.name+": playing "+path)
          sound = pygame.mixer.Sound(file=path)
          os.unlink(path)
        l = random.uniform(phraseMinVol,phraseMaxVol);
        r = l
        soundTrack.playSound(sound,l,r)
      except Exception as e:
        syslog.syslog(self.name+": error on "+phrase+":"+str(e))
      nt = random.randint(soundTrack.eventMin,soundTrack.eventMax)/1000.0;
      syslog.syslog(self.name+": next phrase: "+str(nt))
      time.sleep(nt)




