#!/usr/bin/env python
import pygame
import sys
import syslog
import time
import os
debug = False

screen=None
myFont=None
lineSpace=None
lineLen=None


def displayText(text):
  global screen
  global myFont
  global lineSpace
  global lineLen

  if myFont is None:
    fontSize = 200
    lineSpace = 4
    lineLen = 16
    myFont = pygame.font.Font("../fonts/Watchword_bold_demo.otf", fontSize)
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

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
  wordRect = pygame.Surface((maxWidth,(maxHeight*numLabels)+(lineSpace*numLabels-1)))

  i = 0
  for l in labels:
    h = l.get_height()
    w = l.get_width()
    offset = (wordRect.get_width() - w)/2
    wordRect.blit(l,(offset,i*h + i*lineSpace))
    i += 1
  sx = (screen.get_width() - wordRect.get_width()) / 2
  sy = (screen.get_height() - wordRect.get_height()) / 2
  screen.blit(wordRect,(sx,sy))
  pygame.display.flip() 

if __name__ == '__main__':
  displayText(sys.argv[1])
