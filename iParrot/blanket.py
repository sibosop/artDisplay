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

debug = False


screen=None
myFont=None
lineLen=None
choke = 0

FontFile = "../fonts/Watchword_bold_demo.otf"
FilterDot = True
FontSize = 90

#FontFile = "../fonts/Dry_Brush.ttf"
#FilterDot = False
#FontSize = 60

listMax = 20
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
    lineLen = 30
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
    lines = lines[0:8]
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
      input = self.source.get()
      if debug: syslog.syslog(self.name+" got "+ input)
      if input not in list:
        list.append(input)
        if len(list) > listMax:
          del list[0]
        changed = True


      if changed:
        changed = False
        syslog.syslog(self.name+": "+str(list))
        sendString = ""
        for w in list:
          sendString += " " + w
        self.displayText(sendString)
        time.sleep(choke)
          

  def get(self):
    return self.queue.get()

  
