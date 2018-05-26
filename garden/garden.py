#!/usr/bin/env python
import os
import datetime
import gardenTrack
home = os.environ['HOME']
import sys
import time

if __name__ == '__main__':
  pname = sys.argv[0]
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  print(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  gardenTrack.changeNumGardenThreads(1)
  threads = gardenTrack.eventThreads
  for t in threads:
    t.setCurrentDir(sys.argv[1])
    ct ={ 'file':'a1.wav'}
    t.setCurrentSound(ct)
  while True:
    time.sleep(1)

