#!/usr/bin/env python
import collections
import csv
import os
import sys
import glob
import random
import syslog
import copy
import threading
import json
import shutil
import gardenTrack

debug=True
listMutex=threading.Lock()
maxEvents = 2


rows = ['name','enabled','maxVol']
FileEntry=collections.namedtuple('FileEntry',rows)

fileCollections = {}
fileList=collections.OrderedDict();
edir = ""
defaultKey = "EventCtrl.csv"
eventKey = defaultKey
eventFile = edir + "/" + eventKey
currentCollection = eventKey

def setEdir(d):
  global edir
  global eventFile
  global eventKey
  global currentCollection
  edir = d
  defaultKey = "EventCtrl.csv"
  eventKey = defaultKey
  eventFile = edir + "/" + eventKey
  currentCollection = eventKey

  


def setMaxEvents(m):
  global maxEvents
  test = int(m)
  if test > 0:
    maxEvents = test
  if debug: print("setMaxEvents maxEvents:"+str(maxEvents))
  status = { 'status' : 'ok' }
  rval = json.dumps(status)
  return rval 

def getCurrentCollection():
  return currentCollection

def getFileCollections():
  global fileCollections
  global fileList
  csvFiles = glob.glob(edir+"/*.csv")
  for cf in csvFiles:
    n = cf.split("/")[-1]
    if debug: print("collection file:"+n)
    if ( cf == eventFile ):
      fileCollections[n] = fileList
    else:
      try:
        if debug: print("reading:"+cf)
        with open(cf,"r") as f:
          reader = csv.reader(f)
          fList=collections.OrderedDict();
          e = collections.namedtuple("FileEntry",next(reader))
          for data in map(e._make, reader):
            fList[data.name] = data
          fileCollections[n] = fList;
      except IOError: 
        print("can't open:"+cf);
      

def getCollectionList():
  global fileList
  global fileCollections
  if debug: print("getCollectionList")
  flen = len(fileList)
  if flen == 0:
    createFileList()
    flen = len(fileList)
  collections = [];
  for k in sorted(fileCollections.keys()):
      if debug: print("found collection:"+str(k))
      collections.append(k)
  status = { 'status' : 'ok' , 'collections' : collections }
  rval = json.dumps(status)
  #if debug: print("getSoundList():"+rval)
  return rval 

def setCurrentCollection(col):
  global currentCollection
  global filecollections
  print("setting current collection to:"+col);
  status = { 'status' : 'ok' }
  if col in fileCollections.keys():
    currentCollection = col
  else:
    status['status'] = "fail"
  rval = json.dumps(status)
  if debug: print("setCurrentCollection():"+rval)
  return rval 


def refresh():
  global fileList
  listMutex.acquire()
  fileList=collections.OrderedDict();
  listMutex.release()
  rval = True
  try:
    if debug: print("reading:"+eventFile)
    with open(eventFile,"r") as f:
      reader = csv.reader(f)
      e = collections.namedtuple("FileEntry",next(reader))
      for data in map(e._make, reader):
        listMutex.acquire()
        fileList[data.name] = data
        listMutex.release()
  except IOError: 
    print("can't open:"+eventFile);
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
      fe = FileEntry(name=n, enabled="1", maxVol=gardenTrack.eventMaxVol)
      newList[n] = fe
  fileList = copy.deepcopy(newList)
  try:
    if debug: print("writing:"+eventFile)
    with open(eventFile,'w') as f:
      w = csv.writer(f)
      w.writerow(rows)
      w.writerows([(d.name, d.enabled, d.maxVol) for d in sorted(fileList.values())])
  except IOError: 
    print("can't open for write:"+eventFile);
  listMutex.release()
  getFileCollections()

def createFileList():
  if refresh() is False:
    rescan()
  else:
    getFileCollections()

      
def getSoundList():
  global fileList
  if debug: print("getSoundList")
  flen = len(fileList)
  if flen == 0:
    createFileList()
    flen = len(fileList)
  sounds = [];
  for k in sorted(fileList.keys()):
      s = { 'name' : fileList[k].name 
          , 'enabled' : fileList[k].enabled
          , 'maxVol' : fileList[k].maxVol }
      sounds.append(s)
  status = { 'status' : 'ok' , 'sounds' : sounds }
  rval = json.dumps(status)
  #if debug: print("getSoundList():"+rval)
  return rval 

def saveFileList():
  global fileList
  global eventFile
  global edir
  global rows

  tmpFile = edir + "/tmpfile.csv"
  try:
    with open(tmpFile,'w') as f:
      w = csv.writer(f)
      w.writerow(rows)
      w.writerows([(d.name, d.enabled, d.maxVol) for d in fileList.values()])
    shutil.move(tmpFile,eventFile)
  except Exception, e: 
    print("saveFile error"+repr(str(e)));


def setSoundEnable(name,v):
  global fileList
  status = "fail"
  val = "0"
  if debug: print("setSoundEnable:"+name+" "+v)
  if name in fileList:
    if v == "True":
      val = "1"
    if debug: print("current:"+name+":"+str(fileList[name].enabled))
    item = fileList[name]
    fileList[name] = FileEntry(item.name,val,item.maxVol)
    saveFileList();
    status = "ok"
  return soundServer.jsonStatus(status)


def getSoundEntry():
  global fileList
  global defaultKey
  global currentCollection
  global fileCollections
  flen = len(fileList)
  if flen == 0:
    createFileList()
    flen = len(fileList)
  keys = fileCollections[currentCollection].keys()
  if debug: print("currentCollection:"+currentCollection+" number of keys:"+str(len(keys)))
  done = False
  choice = 0
  if currentCollection == defaultKey:
    choices = 0
    numChoices = random.randint(1,maxEvents)
    if debug: print("default collection:"+currentCollection+" number of choices:"+str(numChoices)+" max Events:"+str(maxEvents))
    rval = []
    while choices < numChoices:
      choice = random.randint(0,len(keys)-1)
      if fileCollections[currentCollection][keys[choice]].enabled == "1":
        choices += 1
        rval.append(fileCollections[currentCollection][keys[choice]].name)
        if debug: print("default collection rval:"+str(rval))
    return rval
  while not done:
    choice = random.randint(0,len(keys)-1)
    if fileCollections[currentCollection][keys[choice]].enabled == "1":
      done = True
  return fileCollections[currentCollection][keys[choice]].name.split('&')
  


if __name__ == '__main__':
  for x in range(0,10):
    entry = getSoundEntry()
    print entry
  rescan()
  for x in range(0,10):
    entry = getSoundEntry()
    print entry
  getFileCollections()
  fcKeys = fileCollections.keys()
  for f in fcKeys:
    print f
    ekeys = fileCollections[f].keys()
    for k in ekeys:
      print fileCollections[f][k]

