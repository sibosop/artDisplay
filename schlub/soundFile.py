#!/usr/bin/env python
import collections
import csv
import os
import sys
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import adGlobal
import glob
import soundTrack
import random

FileEntry=collections.namedtuple('FileEntry',['name','enabled','maxVol'])

fileList=[]

def createFileList():
  global fileList
  edir = adGlobal.eventDir
  files = glob.glob(edir+"/*.wav")
  for f in files:
    n = f.split("/")[-1]
    fileList.append(FileEntry(name=n, enabled=1, maxVol=soundTrack.eventMaxVol))

def getSoundEntry():
  global fileList
  flen = len(fileList)
  if flen == 0:
    createFileList()
    flen = len(fileList)
  choice = random.randint(0,flen-1)
  return fileList[choice]





if __name__ == '__main__':
  for x in range(0,10):
    entry = getSoundEntry()
    print entry
