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

screen=None
myfont=None
setupDone=False
Gran=500
count=0
voiceSound=None
voiceExt = ".wav"

TimerEvent = pygame.USEREVENT
VoiceDoneEvent = pygame.USEREVENT+1
VoiceReadyEvent = pygame.USEREVENT+2
EventDoneEvent=pygame.USEREVENT+4
EventReadyEvent=pygame.USEREVENT+5
EventReadyEvent2=pygame.USEREVENT+6
EventDoneEvent2=pygame.USEREVENT+7
eventSounds=None
maxETimestamp=0
eventMin=1000
eventMax=5000
backgroundCount=0


def playEvent():
  global backgroundCount
  eventChan=pygame.mixer.find_channel()
  if eventChan is None:
    return;
  soundBad=True
  while soundBad:
    done = False
    while not done:
      syslog.syslog("eventdir ="+adGlobal.eventDir)
      filenames = next(os.walk( adGlobal.eventDir))[2]
      choice = random.choice(filenames)
      done = isWav(choice)

    choice = adGlobal.eventDir+choice
    syslog.syslog("soundTrack choice:"+choice)
    try:
      sound = pygame.mixer.Sound(file=choice)
      soundBad = False
      syslog.syslog(choice+" len:"+str(sound.get_length())
            + " backgroundCount:"+str(backgroundCount))
      if sound.get_length() > 50:
        if backgroundCount == 0:
          backgroundCount = 8
          syslog.syslog("playing"+choice+" len:"+str(sound.get_length()))
        else:
          syslog.syslog("skipping"+choice+" len:"+str(sound.get_length()))
          soundBad = True
    except Exception as e:
      syslog.syslog("error on Sound file:"+str(e))

  eventChan.set_volume(random.random(),random.random())
  eventChan.play(sound)
  eventChan.set_endevent()

  
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
  
def setup():
  global screen
  global myfont
  global setupDone
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
      file=None
      while file is None:
        file=textSpeaker.makeSpeakFile(speakText)
      voiceSound = pygame.mixer.Sound(file)
      voiceChan = pygame.mixer.find_channel(True)
      voiceChan.set_endevent(VoiceDoneEvent);
      voiceChan.set_volume(random.random(),random.random())
      voiceChan.play(voiceSound,loops=0)
      os.unlink(file)
    return rval
  
def dispTextChecker():
    global voiceSound
    global backgroundCount
    setup()
    imageDir=adGlobal.imageDir
    count=0
    syslog.syslog("disp text checker started successfully")
    if master.hasAudio():
      pygame.time.set_timer(EventReadyEvent
                  , random.randint(eventMin,eventMax))
    while True:
      for event in pygame.event.get():
        if event.type == TimerEvent:
          if debug: syslog.syslog("TimerEvent:"+str(event))
          if checkText():
            if backgroundCount != 0:
              backgroundCount -= 1
        elif event.type == VoiceDoneEvent:
          voiceTimeout = random.randint(10000,20000)
          if debugSoundTrack: syslog.syslog("VoiceDone replay:"+str(voiceTimeout));
          pygame.time.set_timer(VoiceReadyEvent, int(voiceTimeout))
        elif event.type == VoiceReadyEvent:
          pygame.time.set_timer(VoiceReadyEvent, 0)
          if master.hasAudio():
            if debugSoundTrack: syslog.syslog("VoiceReadyEvent replay");
            voiceChan = pygame.mixer.find_channel(True)
            voiceChan.set_endevent(VoiceDoneEvent);
            voiceChan.set_volume(random.random(),random.random())
            voiceChan.play(voiceSound)
        elif event.type == EventReadyEvent:
          pygame.time.set_timer(EventReadyEvent
                    , random.randint(eventMin,eventMax))
          playEvent()
        elif event.type == pygame.QUIT:
          return
        else:
          syslog.syslog("unknown event:"+str(event))

if __name__ == '__main__':
      dispTextChecker()
