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



fileCollections = []
currentCollection = ""
rootDir = os.environ['GARDEN_ROOT_DIR']
  
for root, dirs, files in os.walk(rootDir):
  for n in dirs:
    if n == "." or n == "..":
      continue
    if debug: print "Found collection:",n
    fileCollections.append(n)
      
for f in fileCollections:
  if debug: print f
if len(fileCollections) != 0:
  currentCollection = fileCollections[0]
if debug: print "currentCollection:",currentCollection


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
  return fileCollections
      
def setCurrentCollection(col):
  global currentCollection
  global fileCollections
  rval = False
  if col in fileCollections:
    currentCollection = col
    rval = True
  return rval 




def getSoundEntry():
  global currentCollection
  global fileCollections
  
  colDir = rootDir + "/" + currentCollection
  if debug: print "colDir:",colDir
  keys = glob.glob(colDir+"/*.wav")
  
  if debug: print "currentCollection:",currentCollection,"number of keys:",len(keys)
  done = False
  choices = 0
  numChoices = random.randint(1,maxEvents)
  if debug: print "collection:",currentCollection," number of choices:",numChoices," max Events:",maxEvents
  rval = []
  for choices in range(numChoices):
    choice = random.randint(0,len(keys)-1)
    rval.append(keys[choice])
  return rval
  


if __name__ == '__main__':
  print getFileCollections()
  print getCurrentCollection()
  print getSoundEntry()

