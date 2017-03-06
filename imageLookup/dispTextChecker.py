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
debug = False
debugFound = True
debugSoundTrack=True
debugSoundTrack=True

screen=None
myfont=None
setupDone=False
Gran=500
count=0
voiceChan=None
voiceSound=None
voiceExt = ".wav"

TimerEvent = pygame.USEREVENT
VoiceDoneEvent = pygame.USEREVENT+1
VoiceReadyEvent = pygame.USEREVENT+2
BackgroundDoneEvent = pygame.USEREVENT+3
EventDoneEvent=pygame.USEREVENT+4
EventReadyEvent=pygame.USEREVENT+5
backgroundSound=None
backgroundChan=None
eventChan=None
eventSounds=None

def setNewSoundTrack():
  global backgroundSound
  global backgroundChan
  filenames = next(os.walk( adGlobal.backgroundDir))[2]
  choice = random.choice(filenames)
  if debugSoundTrack: syslog.syslog("setNewSoundTrack background file choice:"+choice)
  backgroundSound = pygame.mixer.Sound(adGlobal.backgroundDir+choice)
  if backgroundChan is None:
    backgroundChan = pygame.mixer.Channel(1)
    backgroundChan.set_volume(0.2)
    backgroundChan.play(backgroundSound,fade_ms=5000)
  else:
    backgroundChan.fadeout(2000)
  backgroundChan.set_endevent(BackgroundDoneEvent)

def playEvent():
  numEvents = len(eventSounds)
  choice = random.randint(0,numEvents-1) 
  syslog.syslog("soundTrack numEvents:"+str(numEvents)+" choice:"+str(choice))
  sound  = eventSounds[choice]
  eventChan.set_volume(random.random(),random.random())
  eventChan.set_endevent(EventDoneEvent)
  eventChan.play(sound)

  

def newEvents():
  global eventSounds
  global eventChan
  syslog.syslog("new events")
  if eventSounds is None:
    eventSounds=[]
    syslog.syslog("eventdir ="+adGlobal.eventDir)
    filenames = next(os.walk( adGlobal.eventDir))[2]
    for f in filenames:
      sfile=adGlobal.eventDir+f
      syslog.syslog("sountrack loading:"+sfile)
      eventSounds.append(pygame.mixer.Sound(sfile))
    if eventChan is None:
     eventChan = pygame.mixer.Channel(2)
    pygame.time.set_timer(EventReadyEvent, random.randint(100,4000))
    
    





def setup():
  global screen
  global myfont
  global setupDone
  global voiceChan
  if setupDone:
      return
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
  pygame.time.set_timer(TimerEvent, int(Gran))
  voiceChan = pygame.mixer.Channel(0)
  setupDone = True

def newVoice():
  # test for new voice track
  filenames = next(os.walk( adGlobal.voiceDir))[2]
  for f in filenames:
    if debug:
      syslog.syslog( "newVoice: filename:"+f )
    try:
      ext = f.rindex(voiceExt)
    except ValueError:
      if debug:
        syslog.syslog( "newVoice: not lookup text file" )
      continue
    flag = f[ext:]
    if flag == voiceExt:
      if debug: syslog.syslog("newVoice found voice file:"+f)
      fname = adGlobal.voiceDir + "/" + f
      os.unlink(fname)

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

def checkText():
  global count
  global voiceChan
  global voiceSound
  rval = False
  if debug: 
    count += 1
    syslog.syslog( "disp text checking for text. count:"+str(count) )
  text = textChecker.getText();
  if text == None:
    if debug:
        syslog.syslog( "disp text no text" )
  else:
    rval = True
    if debugFound:
        syslog.syslog("disp text found text:"+str(text))
    printText(text)
    if master.hasAudio():
      speakText = text[0]+" "+text[1]
      file=textSpeaker.makeSpeakFile(speakText)
      voiceSound = pygame.mixer.Sound(file)
      voiceChan.stop()
      voiceChan.set_endevent(VoiceDoneEvent);
      voiceChan.set_volume(random.random(),random.random())
      voiceChan.play(voiceSound,loops=0)
      os.unlink(file)
    return rval
  
def dispTextChecker():
    global voiceChan
    global voiceSound
    setup()
    imageDir=adGlobal.imageDir
    count=0
    syslog.syslog("disp text checker started successfully")
    while True:
      for event in pygame.event.get():
        if event.type == TimerEvent:
          if debug: syslog.syslog("TimerEvent:"+str(event))
          if checkText():
            if master.hasAudio():
              syslog.syslog("calling new voice")
              setNewSoundTrack()
              newEvents()
        elif event.type == VoiceDoneEvent:
          pygame.time.set_timer(VoiceReadyEvent, 0)
          voiceTimeout = random.randint(4000,10000)
          if debug: syslog.syslog("VoiceDone replay:"+str(voiceTimeout));
          pygame.time.set_timer(VoiceReadyEvent, int(voiceTimeout))
        elif event.type == VoiceReadyEvent:
          if master.hasAudio():
            if debug: syslog.syslog("VoiceReadyEvent replay");
            voiceChan.set_volume(random.random(),random.random())
            voiceChan.play(voiceSound)
        elif event.type == BackgroundDoneEvent:
          syslog.syslog("backgroundDoneEvent");
          backgroundChan.play(backgroundSound,fade_ms=5000)
        elif event.type == EventDoneEvent:
          nextTime = random.randint(3000,10000)
          syslog.syslog("EventDoneEvent:"+str(event)+" nextTime:"+str(nextTime))
          pygame.time.set_timer(EventReadyEvent, nextTime)
        elif event.type == EventReadyEvent:
          playEvent()
        elif event.type == pygame.QUIT:
          return
        else:
          syslog.syslog("unknown event:"+str(event))

if __name__ == '__main__':
      dispTextChecker()
