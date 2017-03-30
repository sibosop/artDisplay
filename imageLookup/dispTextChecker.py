#!/usr/bin/env python
import textChecker
import pygame
import sys
import adGlobal
import syslog
import time
import master
import textSpeaker
import random
import os
import threading
import soundTrack as st
debug = False
debugFound = True
debugVoiceTrack = True

screen=None
myfont=None
count=0
voiceExt = ".wav"
voiceMutex=threading.Lock()
voiceSound = None
voiceChangeFlag=False
voiceMinVol=.7

maxEventThreads=3
  
def printText(text):
    global screen
    global myfont
    # render text
    lineSpacing = adGlobal.lineSpacing
    label1 = myfont.render(text[0], 1, (255,255,0))
    label2 = myfont.render(text[1], 1, (255,255,0))
    maxWidth = max(label1.get_width(),label2.get_width())
    maxHeight = label1.get_height() + label2.get_height() + lineSpacing 
    wordRect = pygame.Surface((maxWidth,maxHeight))
    screen.fill((0,0,0));
    if maxWidth == label1.get_width():
        wordRect.blit(label1, (0, 0))
        offset = (maxWidth - label2.get_width()) / 2
        wordRect.blit(label2, (offset, label1.get_height() + lineSpacing))
    else:
        offset = (maxWidth - label1.get_width()) / 2
        wordRect.blit(label1, (offset, 0))
        wordRect.blit(label2, (0, label1.get_height() + lineSpacing))

    wx = (screen.get_width() - wordRect.get_width()) / 2
    if wx < 0: 
        wx = 0
    wy = (screen.get_height() - wordRect.get_height()) / 2
    if wy < 0:
        wy = 0
    screen.blit(wordRect,(wx,wy)) 
    pygame.display.flip() 

class checkVoice(threading.Thread):
  def run(self):
    global voiceSound
    global voiceMutex
    global voiceChanged
    while True:
      voiceMutex.acquire()
      vt = voiceSound
      voiceMutex.release()
      if voiceSound is None:
        syslog.syslog("check voice no voice")
        time.sleep(1)
      else:
        syslog.syslog("check voice found voice")
        reps = 0
        if random.randint(0,1) == 0:
          reps = random.randint(2,4)
        else:
          reps = 1
        if debugVoiceTrack:syslog.syslog("VoiceReadyEvent reps:"+str(reps))
        for i in range(reps):
          l = (random.random()*(1.0-voiceMinVol))+voiceMinVol
          r = (random.random()*(1.0-voiceMinVol))+voiceMinVol
          voiceMutex.acquire()
          st.playSound(voiceSound,l,r)
          voiceMutex.release()
          if reps > 1:
            s = random.random()
            time.sleep(s)
        voiceTimeout = random.randint(5,10)
        if debugVoiceTrack: syslog.syslog("Next Voice:"+str(voiceTimeout));
        for i in range(voiceTimeout):
          voiceMutex.acquire()
          c = voiceChanged
          voiceChanged = False
          voiceMutex.release()
          if c:
            syslog.syslog("voiceSound changed")
            break;
          time.sleep(1)

class checkText(threading.Thread):
  def run(self):
    global voiceSound
    global voiceMutex
    global voiceChanged
    while True:
      if debug: 
        count += 1
        syslog.syslog( "disp text checking for text. count:"+str(count) )
      text = textChecker.getText();
      if text == None:
        if debug:
          syslog.syslog( "disp text no text" )
          time.sleep(2)
      else:
        if debugFound:
            syslog.syslog("disp text found text:"+str(text))
        printText(text)
        if master.hasAudio():
          speakText = text[0]+" "+text[1]
          file=None
          while file is None:
            file=textSpeaker.makeSpeakFile(speakText)
          syslog.syslog("voice sound set to:"+file)
          voiceMutex.acquire()
          voiceSound = pygame.mixer.Sound(file)
          voiceChanged = True
          if st.backgroundCount != 0:
              st.backgroundCount -= 1
          voiceMutex.release()
          syslog.syslog("checkText unlinking"+file+" voiceSound:"+str(voiceSound))
          os.unlink(file)
          
def setup():
  global screen
  global myfont
  global setupDone
  hasAudio = master.hasAudio()
  if hasAudio:
      st.setup()
  pygame.init()
  pygame.mouse.set_visible(False);
  screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
  myfont = pygame.font.Font(adGlobal.fontDir + "/Watchword_bold_demo.otf", 200)
  pygame.init()
  if hasAudio:
    syslog.syslog("soundTrack:"+str( pygame.mixer.get_init() ))

eventThreads=[]
def startEventThread(t):
  global eventThreads
  eventThreads.append(t)
  eventThreads[-1].setDaemon(True)
  eventThreads[-1].start()

def dispTextChecker():
  setup()
  imageDir=adGlobal.imageDir
  count=0
  syslog.syslog("disp text checker started successfully")
  startEventThread(checkText())
  if master.hasAudio():
  #  for i in range(maxEventThreads):
  #    startEventThread(st.playEvent())
    startEventThread(checkVoice())
  while True:
    for t in eventThreads:
      t.join(1)  
    time.sleep(4)

if __name__ == '__main__':
  dispTextChecker()
