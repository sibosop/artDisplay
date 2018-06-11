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
import time

debug=True
listMutex=threading.Lock()
maxEvents = 2


orderFile = "order.txt"
fileCollections = []
currentCollection = ""
rootDir = os.environ['GARDEN_ROOT_DIR']
collectionOrder = {}

orderPath = rootDir+"/"+orderFile
if not os.path.exists(orderPath):
  raise Exception(orderPath+" does not exist")
  
with open(orderPath) as f:
  collectionOrder = json.load(f)
    
if 'dirs' not in collectionOrder:
  raise Exception("no dirs in order file")
for d in collectionOrder['dirs']:
  if 'time' not in d:
    raise Exception("no time spec in "+d)
  if 'name' not in d:
    raise Exception("no name spec in "+d) 
    
  
if debug: print collectionOrder
currentCollection = collectionOrder['dirs'].pop(0)
if debug: print "currentCollection:",currentCollection

timeout = time.time() + currentCollection['time']


def setMaxEvents(m):
  global maxEvents
  test = int(m)
  if test > 0:
    maxEvents = test
  if debug: print("setMaxEvents maxEvents:"+str(maxEvents))
  status = { 'status' : 'ok' }
  rval = json.dumps(status)
  return rval 
      
def testBumpCollection():
  global timeout
  global currentCollection
  if time.time() > timeout:
    if len(collectionOrder['dirs']) == 0:
      return False
    timeout = time.time() + currentCollection['time']
    currentCollection = collectionOrder['dirs'].pop(0)
    print "new current collection",currentCollection
  return True
    
  




def getSoundEntry():
  global currentCollection
  global fileCollections
  
  colDir = rootDir + "/" + currentCollection['name']
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
  while testBumpCollection():
    print "currentCollection:",currentCollection
    time.sleep(1)

