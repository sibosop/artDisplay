#!/usr/bin/env python
import os
import datetime
import gardenTrack
import gardenPlayer
import gardenSoundFile
import sys
import random


import time
import gardenPlayer

if __name__ == '__main__':
  random.seed()
  pname = sys.argv[0]
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  print(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))  
  
  gardenTrack.setup()
  gardenTrack.changeNumGardenThreads(4)
  threads = gardenTrack.eventThreads
  pt = gardenPlayer.playerThread(threads)
  pt.setDaemon(True)
  pt.start()
  while True:
    time.sleep(1)
    if pt.done:
      break
  print "garden done"

