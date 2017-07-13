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
import syslog
import copy
import threading

debug=True
listMutex=threading.Lock()

rows = ['name','enabled','maxVol']
FileEntry=collections.namedtuple('FileEntry',rows)

fileList=collections.OrderedDict();
edir = adGlobal.eventDir
eventFile = edir + "/EventCtrl.csv"

def refresh():
  global fileList
  listMutex.acquire()
  fileList=collections.OrderedDict();
  listMutex.release()
  rval = True
  try:
    if debug: syslog.syslog("reading:"+eventFile)
    with open(eventFile,"r") as f:
      reader = csv.reader(f)
      e = collections.namedtuple("FileEntry",next(reader))
      for data in map(e._make, reader):
        listMutex.acquire()
        fileList[data.name] = data
        listMutex.release()
  except IOError: 
    syslog.syslog("can't open:"+eventFile);
    rval = False
  return rval

def rescan():
  global fileList
  listMutex.acquire()
  files = glob.glob(edir+"/*.wav")
  newList=collections.OrderedDict();
  for f in files:
    n = f.split("/")[-1]
    if n in fileList:
      newList[n]=fileList[n]
    else:
      fe = FileEntry(name=n, enabled=1, maxVol=soundTrack.eventMaxVol)
      newList[n] = fe
  fileList = copy.deepcopy(newList)
  try:
    if debug: syslog.syslog("writing:"+eventFile)
    with open(eventFile,'w') as f:
      w = csv.writer(f)
      w.writerow(rows)
      w.writerows([(d.name, d.enabled, d.maxVol) for d in fileList.values()])
  except IOError: 
    syslog.syslog("can't open for write:"+eventFile);
  listMutex.release()

def createFileList():
  if refresh() is False:
    rescan()
      

def getSoundEntry():
  global fileList
  flen = len(fileList)
  if flen == 0:
    createFileList()
    flen = len(fileList)
  keys = fileList.keys()
  choice = random.randint(0,len(keys)-1)
  return fileList[keys[choice]]


if __name__ == '__main__':
  for x in range(0,10):
    entry = getSoundEntry()
    print entry
  rescan()
  for x in range(0,10):
    entry = getSoundEntry()
    print entry
