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

import syslog
import time
import random
import re
import displayText
import textSpeaker
import pygame

debug = False
poemQueue=[]
queueMutex=threading.Lock()




def compilePoem(poem):
  rval = []
  syslog.syslog("compile poem")
  try:
    for l in poem:
      if l == "+++++":
        sound = None
      else:
        file = None
        while file is None:
          file = textSpeaker.makeSpeakFile(l)
        sound = pygame.mixer.Sound(file)
        os.unlink(file)
      rval.append((l,sound));
  except Exception as e:
    syslog.syslog("compile poem: "+str(e))
    rval = []
  return rval

poemGets = [emily.get,shakes.get,browning.get]

class poemQueueThread(threading.Thread):
  def run(self):
    maxQueueSize=3
    global poemQueue
    global queueMutex
    while True:
      queueMutex.acquire()
      l = len(poemQueue)
      queueMutex.release()
      syslog.syslog("queue len:"+str(l))
      if l < maxQueueSize:
        poem = []
        while len(poem) == 0:
          poem = compilePoem(random.choice(poemGets)())
        queueMutex.acquire()
        poemQueue.append(poem)
        queueMutex.release()
      else:
        time.sleep(5)


def playText(sound):
  chan = pygame.mixer.find_channel()
  chan.set_volume(.8,.8)
  chan.play(sound)
  return chan
  
  
class poemLoop(threading.Thread):
  def run(self):
    global poemQueue
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.init()
    pygame.mouse.set_visible(False)
    current = None
    while True:
      qlen = 0
      while qlen == 0:
        queueMutex.acquire()
        qlen = len(poemQueue)
        queueMutex.release()
        if qlen == 0:
          syslog.syslog("waiting for poem queue")
          time.sleep(5)
        else:
          queueMutex.acquire()
          current = poemQueue.pop(0)
          queueMutex.release()
          syslog.syslog("got a poem");
          time.sleep(2)

      for l in current:
        if l[0] == "+++++":
          syslog.syslog("doing sleep")
          time.sleep(2)
          continue
        chan = playText(l[1])
        if debug: syslog.syslog("poem loop:"+l[0])
        displayText.displayText(l[0])
        while chan.get_busy():
          time.sleep(0)
      

if __name__ == '__main__':
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  t = poemQueueThread()
  t.setDaemon(True)
  t.start()
  sl = poemLoop()
  sl.setDaemon(True)
  sl.start()

  while True:
    try:
      time.sleep(1)
    except Exception as e:
      syslog.syslog(os.argv[0]+":"+str(e))
  t.join()
  sl.join()
