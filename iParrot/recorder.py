#!/usr/bin/env python
import threading
import queue
import syslog
import sys
import time
import os
import alsaaudio
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/shared")
import asoundConfig

audioFileTmpPath = home + "/GitProjects/artDisplay/tmp"
tmpRoot = audioFileTmpPath + "/audio"
loopCount = 1000


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
      self.fname = tmpRoot + str(self.fileCount) + ".raw"
      self.f = open(self.fname,'wb')
      loops = loopCount
      self.fileCount += 1
      while loops > 0:
        loops -= 1
        l, data = self.inp.read()
        if l < 0:
          syslog.syslog(self.name+" pipe error")
          continue
        if l:
          self.f.write(data)
        time.sleep(.001)
      loops = loopCount
      self.f.close()
      self.queue.put(self.fname)
      syslog.syslog(self.name+" sending: "+self.fname)

  def close(self):
    self.f.close()
    os.remove(self.fname)

  def get(self):
    return self.queue.get()

  
