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

debug=True

rows = ['name','enabled','maxVol']
FileEntry=collections.namedtuple('FileEntry',rows)

fileList=collections.OrderedDict();

def refresh():
  global fileList
  rval = True
  edir = adGlobal.eventDir
  eventFile = edir+"/EventCtrl.csv"
  fileList = {}
  try:
    if debug: syslog.syslog("reading:"+eventFile)
    with open(eventFile,"r") as f:
      reader = csv.reader(f)
      e = collections.namedtuple("FileEntry",next(reader))
      for data in map(e._make, reader):
        fileList[data.name] = data
  except IOError: 
    syslog.syslog("can't open:"+eventFile);
    rval = False
  return rval


def createFileList():
  global fileList
  edir = adGlobal.eventDir
  eventFile = edir+"/EventCtrl.csv"
  if refresh() is False:
    files = glob.glob(edir+"/*.wav")
    for f in files:
      n = f.split("/")[-1]
      fe = FileEntry(name=n, enabled=1, maxVol=soundTrack.eventMaxVol)
      fileList[fe.name]=fe
    try:
      if debug: syslog.syslog("writing:"+eventFile)
      with open(eventFile,'w') as f:
        w = csv.writer(f)
        w.writerow(rows)
        w.writerows([(d.name, d.enabled, d.maxVol) for d in fileList.values()])
    except IOError: 
      syslog.syslog("can't open for write:"+eventFile);
      

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
  print refresh()
  for x in range(0,10):
    entry = getSoundEntry()
    print entry
