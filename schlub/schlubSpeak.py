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

currentPhrase={}
phraseMutex=threading.Lock()
debug=True
phraseMinVol = 0.7
phraseMaxVol = 1.0

def setPhraseScatter(flag):
  global phraseScatter
  return soundServer.jsonStatus("depreciated")

def setFirst(f):
  global currentPhrase
  phraseMutex.acquire()
  currentPhrase['first'] = f
  phraseMutex.release()

def clearCurrentPhrase():
  global currentPhrase
  phraseMutex.acquire()
  currentPhrase={}
  phraseMutex.release()


def setCurrentPhrase(args):
  global currentPhrase
  args['first'] = True
  phraseMutex.acquire()
  currentPhrase=args
  phraseMutex.release()
  syslog.syslog("current phrase:"+str(currentPhrase))
  if currentPhrase['phrase'] == "":
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
    if debug: syslog.syslog(self.name+": starting")
    dir = adGlobal.eventDir
    oldPhrase = ""
    sound = None
    reps = 0
    phrase = ""
    scatter = False
    lang = ''
    while self.isRunning():
      try:
        phraseArgs = getCurrentPhrase();
        if not phraseArgs:
          #syslog.syslog("waiting for phrase")
          time.sleep(1)
          continue;

        if phraseArgs['first']:
          phrase = phraseArgs['phrase']
          if 'reps' in phraseArgs:
            reps = phraseArgs['reps']
            if reps == 0:
              reps = -1
          else:
            reps = -1
          if 'scatter' in phraseArgs:
            scatter = phraseArgs['scatter']
          else:
            scatter = False

          if 'lang' in phraseArgs:
            lang = phraseArgs['lang']
          else:
            lang = ''
          phrase = phraseArgs['phrase']
          oldPhrase = ""
          setFirst(False)

        if debug: syslog.syslog("reps:"+str(reps)+" scatter:"+str(scatter))

        if phrase == "":
          clearCurrentPhrase()
          continue

        if phrase == "--":
          clearCurrentPhrase();
          time.sleep(1)
          continue
        phrase = phrase.replace("-"," ")
        if debug: syslog.syslog("PhraseScatter:"+str(scatter))
        if scatter:
          phrase = random.choice(phrase.split())
        if oldPhrase != phrase:
          oldPhrase = phrase
          path = textSpeaker.makeSpeakFile(phrase,lang)
          if path is None:
            syslog.syslog("conversion of "+phrase+" failed")
            time.sleep(1)
            continue
          if debug: syslog.syslog(self.name+": playing "+path)
          sound = pygame.mixer.Sound(file=path)
          os.unlink(path)
        l = random.uniform(phraseMinVol,phraseMaxVol);
        r = l
        if reps != 0:
          soundTrack.playSound(sound,l,r)
          if reps != -1:
            reps -= 1
      except Exception as e:
        syslog.syslog(self.name+": error on "+str(phrase)+":"+str(e))
      nt = random.randint(soundTrack.eventMin,soundTrack.eventMax)/1000.0;
      syslog.syslog(self.name+": next phrase: "+str(nt)+" reps:"+str(reps))
      if reps == 0:
        clearCurrentPhrase()
      else:
        time.sleep(nt)




