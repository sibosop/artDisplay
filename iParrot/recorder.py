#!/usr/bin/env python
import threading
import queue
import syslog
import time

class inputThread(threading.Thread):
  def __init__(self):
    super(inputThread,self).__init__()
    self.name = "Input Thread"
    self.queue = queue.Queue()

  def run(self):
    syslog.syslog("starting: "+self.name)
    count = 0
    while True:
      syslog.syslog(self.name+" sending: "+str(count))
      self.queue.put(str(count))
      count += 1
      time.sleep(5)

  def get(self):
    return self.queue.get()

  
