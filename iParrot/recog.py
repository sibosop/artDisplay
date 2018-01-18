#!/usr/bin/env python
import threading
import queue
import time
import syslog

class recogThread(threading.Thread):
  def __init__(self,i):
    super(recogThread,self).__init__()
    self.name = "Recog Thread"
    self.queue = queue.Queue()
    self.source = i

  def run(self):
    syslog.syslog("starting: "+self.name)
    while True:
      input = self.source.get()
      syslog.syslog(self.name+" got "+ input)
      self.queue.put(input)

  def get(self):
    return self.queue.get()

  
