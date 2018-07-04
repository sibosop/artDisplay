#!/usr/bin/env python
import sys
import os
import time
import host

home = os.environ['HOME']
import random
lines = []
init=False
debug = True
def initWords():
  global lines
  if debug: print "init words"
  random.seed()
  wordDir=home+"/GitProjects/artDisplay/lists"
  wordList=["corncob_lowercase.txt"]
  for w in wordList:
    f = open(wordDir+"/"+w,"r")
    for l in f.read().split('\n'):
      lines.append(l)
  init=True


#@profile
def getWords():
  global init
  global lines
  if init==False:
    initWords()
    init=True
  tests=[]
  for i in range(0,2):
    n = random.randint(0,len(lines)-1)
    tests.append(lines[n])
  if debug: print "tests:",tests[0],tests[1] #,tests[2]
  return tests




if __name__ == '__main__':
  hostList = host.getHosts()
  screenList = []
  for h in hostList:
    if h['hasScreen']:
      if host.sendToHost(h['ip'],{'cmd' : 'Probe', 'args' : [""] }):
        screenList.append(h)
        print "adding",h
      else:
        print "skipping:",h
  while True:
    for h in screenList:
      words = getWords()
      phrase = ""
      for w in words:
        phrase += w + " "
        args={}
        args['phrase'] = phrase
      host.sendToHost(h['ip'],{'cmd' : 'Show', 'args' : args })
    time.sleep(5)

