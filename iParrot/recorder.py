#!/usr/bin/env python
import threading
import queue
import syslog
import sys
import time
import os
import alsaaudio
import grpc
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/shared")
import asoundConfig

loopCount = 1000
debug = False

class inputThread(threading.Thread):
  def __init__(self):
    super(inputThread,self).__init__()
    self.name = "Input Thread"
    self.queue = queue.Queue()
    self.fileCount = 0
    self.hw = asoundConfig.getHw()
    self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, cardindex=int(self.hw['Mic']))
    self.inp.setchannels(1)
    self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    self.inp.setperiodsize(1600)

  def run(self):
    syslog.syslog("starting: "+self.name)
    while True:
      loops = loopCount
      buff = bytes()
      while loops > 0:
        loops -= 1
        l, data = self.inp.read()
        if l < 0:
          syslog.syslog(self.name+" pipe error")
          continue
        if l:
          buff += data
        time.sleep(.001)
      loops = loopCount
      self.queue.put(buff)
      if debug: syslog.syslog(self.name+" sending: "+str(len(buff)))

  def close(self):
    return

  def get(self):
    if debug: syslog.syslog(self.name+"get()")
    buff = self.queue.get()
    if debug: syslog.syslog(self.name+"return buff sized:"+str(len(buff)))
    return buff 
  
