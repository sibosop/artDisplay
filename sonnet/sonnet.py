#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
import threading


sys.path.append(home+"/GitProjects/artDisplay/imageLookup")

import syslog
import time
import random
import re
import displayText
import textSpeaker
import pygame

debug = True
numeral_map = None
sonnetQueue=[]
queueMutex=threading.Lock()


def roman_to_int(n):
  n = n.strip()

  reg=re.compile('^[IVXLCDM]+$')
  if reg.match(n) is None:
    #syslog.syslog(n+": not a match")
    return 0
  i = result = 0
  for integer, numeral in numeral_map:
    while n[i:i + len(numeral)] == numeral:
      result += integer
      i += len(numeral)
  return result

def getSonnet():
  global numeral_map
  if numeral_map is None:
    numeral_map = zip(
      (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
      ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    )
  maxSonnet=154
  choice = random.randint(1,154)
  if debug: syslog.syslog("Get Sonnet:"+str(choice))

  found=False
  sonnet = []
 
  with open("wssnt10.txt") as f:
    for line in f:
      if found:
        l = line.strip()
        if len(l) == 0:
          if len(sonnet) != 0:
            l = "Sonnet number "+str(choice)
            sonnet.insert(0,l)
            return (sonnet)
        else:
          sonnet.append(l)
      else:
        test = roman_to_int(line)
        if test==choice:
          if debug: syslog.syslog(line+":"+str(test))
          found = True

  return None


def compileSonnet(sonnet):
  rval = []
  for l in sonnet:
    file = None
    while file is None:
      file = textSpeaker.makeSpeakFile(l)
    sound = pygame.mixer.Sound(file)
    os.unlink(file)
    rval.append((l,sound));
  return rval


class sonnetQueueThread(threading.Thread):
  def run(self):
    maxQueueSize=3
    global sonnetQueue
    global queueMutex
    while True:
      queueMutex.acquire()
      l = len(sonnetQueue)
      queueMutex.release()
      syslog.syslog("queue len:"+str(l))
      if l < maxQueueSize:
        sonnet = compileSonnet(getSonnet())
        queueMutex.acquire()
        sonnetQueue.append(sonnet)
        queueMutex.release()
      time.sleep(1)


def playText(sound):
  chan = pygame.mixer.find_channel()
  chan.set_volume(.8,.8)
  chan.play(sound)
  return chan
  
  
def sonnetLoop():
  global sonnetQueue
  pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
  pygame.init()
  pygame.mouse.set_visible(False)
  current = None
  while True:
    qlen = 0
    while qlen == 0:
      queueMutex.acquire()
      qlen = len(sonnetQueue)
      queueMutex.release()
      if qlen == 0:
        syslog.syslog("waiting for sonnet queue")
        time.sleep(1)
      else:
        queueMutex.acquire()
        current = sonnetQueue.pop(0)
        queueMutex.release()
        syslog.syslog("got a sonnet");
        time.sleep(2)

    first = True
    for l in current:
      chan = playText(l[1])
      displayText.displayText(l[0])
      while chan.get_busy():
        time.sleep(0)
      if first:
        first = False
        time.sleep(2)

if __name__ == '__main__':
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  t = sonnetQueueThread()
  t.setDaemon(True)
  t.start()
  sonnetLoop()
  t.join()
