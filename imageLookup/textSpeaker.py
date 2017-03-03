#!/usr/bin/env python
import textChecker
import pygame
import sys
import adGlobal
import syslog
import time
import master
import os
from gtts import gTTS
from pydub import AudioSegment
debug = True

setupDone=False

def setup():
  global setupDone
  if setupDone:
      return
  pygame.init()
  setupDone=True
  syslog.syslog("sound pygame setup done")

def speak(line):
    if debug: syslog.syslog("speak:"+line);
    try:
      if master.hasAudio() is False:
        if debug: syslog.syslog("speak: no audio");
        return
      setup()
      fnameRoot = "../tmp/" + line 
      if adGlobal.internetOn():
        syslog.syslog("speak: internet on using gTTS");
        if debug: syslog.syslog("playText line:"+line)
        fname = fnameRoot + ".mp3"
        if debug: syslog.syslog("speak:"+fname)
        tts1=gTTS(text=line,lang='en')
        tts1.save(fname)
        if debug: syslog.syslog("speak:"+fname)
        sound = AudioSegment.from_mp3(fname)
        os.unlink(fname)
        fname = fnameRoot + ".wav"
        if debug: syslog.syslog("speak:"+fname)
        sound.export(fname, format="wav")
      else:
        syslog.syslog("speak: internet off using espeak");
        fnameRoot += ".wav"
        if debug: syslog.syslog("speak:"+fnameRoot)
        os.system("espeak -w "+fnameRoot+" "+line)

    except Exception as e:
      syslog("speak error: ", e)


if __name__ == '__main__':
    speak(sys.argv[1])
    
	
