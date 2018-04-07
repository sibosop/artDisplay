#!/usr/bin/env python
import pygame
import sys
import syslog
import time
import os
import os
import sys
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import master
debug = False

screen=None
myFont=None
lineLen=None

FontFile = "../fonts/Watchword_bold_demo.otf"
FilterDot = True
FontSize = 90

#FontFile = "../fonts/Dry_Brush.ttf"
#FilterDot = False
#FontSize = 60


def displayText(text):
  global screen
  global myFont
  global lineLen
  

  if myFont is None:
    if master.isRaspberry:
      screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    else:
      screen = pygame.display.set_mode([800,480]);
      
  if debug: syslog.syslog("displayText setting FontSize:"+str(FontSize))
  lineLen = 16
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
  lines = lines[0:4]
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

if __name__ == '__main__':
  if master.isRaspberry:
    os.environ['DISPLAY']=":0.0"
  pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
  pygame.init()
  pygame.mouse.set_visible(False)
  displayText(sys.argv[1])
  time.sleep(5)
