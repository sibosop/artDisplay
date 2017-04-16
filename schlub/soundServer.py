#!/usr/bin/env python

import threading
import time

class soundServerThread(threading.Thread):
  def run(self):
    while True:
      try:
        time.sleep(1)
      except KeyboardInterrupt:
        return

