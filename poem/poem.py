#!/usr/bin/env python
import os
import roman
home = os.environ['HOME']
import sys
import syslog
import threading
import shakes
import emily
import browning

sys.path.append(home+"/GitProjects/artDisplay/imageLookup")

import master
import syslog
import time
import random
import re
import displayText
import textSpeaker
import pygame
import glob
import json
debug = True

poemDir = "/media/parallels/POEMDATA"
candidates = glob.glob(poemDir+"/*/*/*.txt")

def playText(sound):
  chan = pygame.mixer.find_channel()
  chan.set_volume(.8,.8)
  chan.play(sound)
  return chan

def getPoem():
  global poemDir
  f = random.choice(candidates)
  dirPath = os.path.dirname(f)
  if debug: syslog.syslog("choice:"+f+" dir path:"+dirPath)
  poemFile = open(f,"r")
  jsonStr = poemFile.read()
  poem = json.loads(jsonStr)
  for e in poem:
    if debug: syslog.syslog("text:"+e['text'])
    w = e['file']
    if debug: syslog.syslog("file:"+w)
    if ( w == "None" ):
      time.sleep(2)
    else:
      displayText.displayText(e['text'])
      sound = pygame.mixer.Sound(dirPath+"/"+w)
      chan = pygame.mixer.find_channel()
      chan.set_volume(.5)
      chan.play(sound)
      while ( chan.get_busy() ):
        time.sleep(0)



      

  
    
    
  

  
class poemLoop(threading.Thread):
  def run(self):
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.init()
    pygame.mouse.set_visible(False)
    while True:
      current = getPoem()
      time.sleep(5)
      

if __name__ == '__main__':
  random.seed()
  if master.isRaspberry:
    os.environ['DISPLAY']=":0.0"
    poemDir = "/media/pi/POEMDATA"
  os.chdir(os.path.dirname(sys.argv[0]))
  sl = poemLoop()
  sl.setDaemon(True)
  sl.start()

  while True:
    try:
      time.sleep(1)
    except Exception as e:
      syslog.syslog(sys.argv[0]+":"+str(e))
      break
