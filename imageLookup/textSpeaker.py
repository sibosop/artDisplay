#!/usr/bin/env python
import textChecker
import pygame
import sys
import adGlobal
import syslog
import time
import master
import wave
import os
from gtts import gTTS
from pydub import AudioSegment
debug = True

def makeSpeakFile(line):
  rval = None 
  if debug: syslog.syslog("speak:"+line);
  try:
    if master.hasAudio() is False:
      if debug: syslog.syslog("speak: no audio");
      return rval
    fnameRoot = "../tmp/" + line.replace(" ","_")
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
      rval = fname
    else:
      syslog.syslog("speak: internet off using espeak");
      fname = fnameRoot + ".wav"
      if debug: syslog.syslog("speak:"+fname)
      os.system("espeak -w "+fname+" '"+line+"'")
      rval = fname
  except Exception as e:
    syslog("speak error: ", e)
  return rval


