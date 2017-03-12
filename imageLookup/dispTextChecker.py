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
debug = False
debugFound = True
debugSoundTrack=True

screen=None
myfont=None
count=0
voiceExt = ".wav"

eventMin=100
eventMax=10000
backgroundCount=0
eventTimeThresholdIncrement=.1
initialEventTimeThreshold=1.5
eventTimeThreshold=initialEventTimeThreshold
eventTimeMaxThreshold = 50.0
allowBackgroundThreshold=20.0
backgroundThreshold=90.0
backgroundIgnoreCount=8

maxEventThreads=3
eventMutex=threading.Lock()
voiceMutex=threading.Lock()
voiceSound = None
voiceChangeFlag=False
voiceMinVol=.7
eventMaxVol=.7

def getBusyChannels():
  count = 0
  for i in range(pygame.mixer.get_num_channels()):
    if pygame.mixer.Channel(i).get_busy():
      count +=1
  return count

def isWav(f):
  try:
    ext = f.rindex(".wav")
  except ValueError:
    if debugSoundTrack:
      syslog.syslog(sfile+ ":not wav file")
    return False
  flag = f[ext:]
  if debugSoundTrack:
    syslog.syslog("flag ext = "+flag)
  if flag != ".wav":
    return False
  return True

def makeEventChoice(filenames):
  done = False
  while not done:
    if filenames is None:
      syslog.syslog("eventdir ="+adGlobal.eventDir)
      filenames = next(os.walk( adGlobal.eventDir))[2]
    choice = random.choice(filenames)
    done = isWav(choice)
  return (choice,filenames)


def playSound(sound,l,r):
  eventChan = None
  eventChan=pygame.mixer.find_channel()
  if eventChan is None:
    pygame.mixer.set_num_channels(pygame.mixer.get_num_channels()+1);
    eventChan=pygame.mixer.find_channel()
  syslog.syslog("busy channels:"+str(getBusyChannels()))
  syslog.syslog("l: "+str(l) + " r:"+str(r))
  eventChan.set_volume(l,r)
  eventChan.play(sound)
  eventChan.set_endevent()
  

class playEvent(threading.Thread):
  def run(self):
    global backgroundCount
    global backgroundCount
    global eventTimeThreshold
    global allowBackgroundThreshold
    global backgroundThreshold
    global backgroundIgnoreCount
    global eventTimeThresholdIncrement
    global initialEventTimeThreshold
    global eventTimeMaxThreshold
    global eventMutex
    filenames=None
    syslog.syslog("play event thread")
    while True:
      while True:
        vars = makeEventChoice(filenames)
        filenames = vars[1]
        choice = adGlobal.eventDir+vars[0]
        syslog.syslog("soundTrack choice:"+choice)
        try:
          sound = pygame.mixer.Sound(file=choice)
          len = sound.get_length()
          syslog.syslog(choice+" len:"+str(len)
                + " allowBackgroundThreshold:"+ str(allowBackgroundThreshold)
                + " eventTimeThreshold:"+str(eventTimeThreshold)
                + " backgroundCount:"+str(backgroundCount))
          if eventTimeThreshold > allowBackgroundThreshold and len > backgroundThreshold:
            if backgroundCount == 0:
              backgroundCount = backgroundIgnoreCount
              syslog.syslog("playing"+choice+" len:"+str(len))
              break
            else:
              syslog.syslog("skipping "+choice+" len:"+str(len))
          elif len < eventTimeThreshold:
            syslog.syslog("playing " + choice + " len:"+str(len)
                  +" threshold:"+str(eventTimeThreshold))
            break
          else:
            syslog.syslog("skipping "+choice+" len:"+str(len)
                  +" threshold:"+str(eventTimeThreshold))

        except Exception as e:
          syslog.syslog("error on Sound file:"+str(e))
      l = random.random() * eventMaxVol
      r = random.random() * eventMaxVol
      playSound(sound,l,r)
      eventMutex.acquire()
      eventTimeThreshold += eventTimeThresholdIncrement
      eventMutex.release()
      if  eventTimeThreshold > eventTimeMaxThreshold :
        eventMutex.acquire()
        eventTimeThreshold = initialEventTimeThreshold
        eventMutex.release()
        syslog.syslog("reseting eventTimeThreshold max:"+str(eventTimeMaxThreshold))

      nt = random.randint(eventMin,eventMax)/1000.0;
      syslog.syslog("next play:"+str(nt))
      time.sleep(nt)
      syslog.syslog("back from sleep")

  

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
      syslog.syslog("check voice doing acquire")
      voiceMutex.acquire()
      vt = voiceSound
      syslog.syslog("voiceSound:"+str(vt))
      voiceMutex.release()
      if voiceSound is None:
        syslog.syslog("check voice no voice")
        time.sleep(1)
      else:
        syslog.syslog("check voice found voice")
        reps = 0
        if random.randint(0,3) == 0:
          reps = random.randint(1,3)
        else:
          reps = 1
        if debugSoundTrack:syslog.syslog("VoiceReadyEvent reps:"+str(reps))
        for i in range(reps):
          l = (random.random()*(1.0-voiceMinVol))+voiceMinVol
          r = (random.random()*(1.0-voiceMinVol))+voiceMinVol
          voiceMutex.acquire()
          playSound(voiceSound,l,r)
          voiceMutex.release()
          if reps > 1:
            s = random.random()
            time.sleep(s)
        voiceTimeout = random.randint(10,20)
        if debugSoundTrack: syslog.syslog("Next Voice:"+str(voiceTimeout));
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
          voiceMutex.release()
          syslog.syslog("checkText unlinking"+file+" voiceSound:"+str(voiceSound))
          os.unlink(file)
          
def setup():
  global screen
  global myfont
  global setupDone
  hasAudio = master.hasAudio()
  if hasAudio:
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
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
    for i in range(maxEventThreads):
      startEventThread(playEvent())
    startEventThread(checkVoice())
  while True:
    for t in eventThreads:
      t.join(1)  
    time.sleep(4)

if __name__ == '__main__':
      dispTextChecker()
