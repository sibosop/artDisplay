#!/usr/bin/env python
import os
import datetime
import gardenTrack
import gardenPlayer
import sys


import time
import gardenPlayer

if __name__ == '__main__':
  pname = sys.argv[0]
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  print(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  gardenTrack.setup()
  gardenTrack.changeNumGardenThreads(1)
  threads = gardenTrack.eventThreads
  adGlobal.eventDir = sys.argv[1]
  pt = gardenPlayer.playerThread(threads)
  pt.setDaemon(True)
  pt.start()
  while True:
    time.sleep(1)
