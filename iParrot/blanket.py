#!/usr/bin/env python
import threading
import queue
import time
import syslog

class phraseSender(threading.Thread):
  def __init__(self,i):
    super(phraseSender,self).__init__()
    self.name = "phraseSender"
    self.source = i

  def run(self):
    syslog.syslog("starting: "+self.name)
    while True:
      input = self.source.get()
      syslog.syslog(self.name+" got "+ input)

  def get(self):
    return self.queue.get()

  
