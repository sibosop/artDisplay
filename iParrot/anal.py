#!/usr/bin/env python
import threading
import queue
import time
import syslog

chooseLen=6
debug=False
class analThread(threading.Thread):
  def __init__(self,i):
    super(analThread,self).__init__()
    self.name = "analThread"
    self.queue = queue.Queue()
    self.source = i

  def run(self):
    syslog.syslog("starting: "+self.name)
    while True:
      input = self.source.get()
      if debug: syslog.syslog(self.name+" got "+ input)
      for w in input.split():
        if debug: syslog.syslog(self.name+"test:"+w)
        if len(w) > chooseLen:
          if debug: syslog.syslog(self.name+"CHOSE: "+w)
          self.queue.put(w)

  def get(self):
    return self.queue.get()

  
