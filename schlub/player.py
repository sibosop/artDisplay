#!/usr/bin/env python

import threading
import time

class playerThread(threading.Thread):
  def run(self):
    while True:
      try:
        time.sleep(1)
      except KeyboardInterrupt:
        return
