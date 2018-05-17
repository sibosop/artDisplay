#!/usr/bin/env python
import threading
import queue
import time
import syslog
import pygame
import sys
import os
import master
import time
import urllib2
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/shared")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import slp
import words
import random
import json
import transServer


debug = True


screen=None
myFont=None
lineLen=None
noLines=6
lineLen = 25
choke = 0

transMutex = threading.Lock()



bufferSize=1000
currentTranscript=[]

def setCurrentTranscript(trans):
  global currentTranscript
  global bufferSize

  #transMutex.acquire()
  entry={}
  entry['trans'] = trans['trans']
  entry['confidence'] = trans['confidence']
  entry['timestamp'] = time.time()
  #currentTranscript.append(entry)
  currentTranscript.insert(0,entry)
  if len(currentTranscript) > bufferSize:
    #currentTranscript.pop(0)
    currentTranscript.pop()
  #transMutex.release()
  rval = "ok"
  return transServer.jsonStatus(rval)

def getCurrentTranscript(confThres):
  global currentTranscript
  rval = {}
  rval['status'] = "ok"
  #transMutex.acquire()
  transcript = []
  for e in currentTranscript:
    if e['confidence'] >= int(confThres)/10.0:
      transcript.append(e)
  rval['transcript'] = transcript
  #transMutex.release()
  return json.dumps(rval)

FontFile = "../fonts/Watchword_bold_demo.otf"
FilterDot = True
FontSize = 90

#FontFile = "../fonts/Dry_Brush.ttf"
#FilterDot = False
#FontSize = 60

listMax = 10
os.environ['DISPLAY']=":0.0"

class phraseSender(threading.Thread):
  def __init__(self,i):
    super(phraseSender,self).__init__()
    self.name = "phraseSender"
    self.source = i

  def displayText(self,text):
    global screen
    global myFont
    global lineLen
    
    if myFont is None:
      pygame.init()
      screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

    if debug: syslog.syslog("displayText setting FontSize:"+str(FontSize))
    myFont = pygame.font.Font(FontFile, FontSize)

    if FilterDot:
      text=text.replace("."," ")
    text=text.strip()
    words=text.split()
    lines = []
    r = ""
    for w in words:
      if (len(w) + len(r)) < lineLen:
        r += w + " "
      else:
        lines.append(r)
        r = w + " "
    lines.append(r)
    lines = lines[0:noLines]
    i = 0
    screen.fill((0,0,0))
    labels = []
    maxWidth = 0
    maxHeight = 0
    for l in lines:
      label = myFont.render(l, 1, (255,255,0))
      w = label.get_width()
      h = label.get_height()
      maxWidth = max(w,maxWidth)
      maxHeight = max(h,maxHeight)
      labels.append(label)
        
    numLabels = len(labels)
    wordRect = pygame.Surface((maxWidth,(maxHeight*numLabels)-4))

    i = 0
    for l in labels:
      h = l.get_height()
      w = l.get_width()
      offset = (wordRect.get_width() - w)/2
      wordRect.blit(l,(offset,i*h))
      i += 1
    sx = (screen.get_width() - wordRect.get_width()) / 2
    sy = (screen.get_height() - wordRect.get_height()) / 2
    screen.blit(wordRect,(sx,sy))
    pygame.display.flip() 

  def run(self):
    syslog.syslog("starting: "+self.name)
    list = []
    changed = False
    while True:
      #try:
        input = self.source.get()
        if debug: syslog.syslog(self.name+" got "+ str(input))
        self.displayText(input['trans'])
        setCurrentTranscript(input)
      #except Exception, e:
         #syslog.syslog(self.name+"phrasePlayerError:"+repr(e));
          

  def get(self):
    return self.queue.get()

  
