#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys


sys.path.append(home+"/GitProjects/artDisplay/imageLookup")

import syslog
import time
import random
import re
import displayText
import textSpeaker
import pygame

debug = False
numeral_map = None
current = None

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

GetSonnetEvent=pygame.USEREVENT
LineDoneEvent=pygame.USEREVENT+1
SonnetWaitEvent=pygame.USEREVENT+2

def playText(l):
  file = None
  while file is None:
    file = textSpeaker.makeSpeakFile(l)
  sound = pygame.mixer.Sound(file)
  os.unlink(file)
  chan = pygame.mixer.find_channel()
  chan.set_endevent(LineDoneEvent)
  chan.set_volume(.8,.8)
  chan.play(sound)
  
  
def nextLine():
  global current
  if len(current) == 0:
    pygame.time.set_timer(SonnetWaitEvent,random.randint(2000,5000))
  else:
    l = current.pop(0)
    playText(l)
    displayText.displayText(l)

def sonnetLoop():
  global current
  pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
  pygame.init()
  pygame.mouse.set_visible(False)
  pygame.event.post(pygame.event.Event(GetSonnetEvent))
  while True:
    for event in pygame.event.get():
      syslog.syslog("event:"+str(event))
      if event.type == GetSonnetEvent:
        current = getSonnet()
        nextLine()
      elif event.type == LineDoneEvent:
        nextLine()
      elif event.type == SonnetWaitEvent:
        pygame.time.set_timer(SonnetWaitEvent,0)
        pygame.event.post(pygame.event.Event(GetSonnetEvent))
      else:
        syslog.syslog("unknown event:"+str(event))

if __name__ == '__main__':
  sonnetLoop()
