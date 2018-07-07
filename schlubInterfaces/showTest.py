#!/usr/bin/env python
import sys
import os
import time
import host
import json
import argparse

home = os.environ['HOME']
import random
lines = []
init=False
debug = False
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

def getPhrase():
  rval = {}
  words = getWords()
  phrase = ""
  for w in words:
    phrase += w + " "
  rval['phrase'] = phrase
  return rval

langs=["en", "en-au", "en-uk" ]

def setPhraseParms(args):
  args['lang'] = random.choice(langs)
  args['reps'] = random.randint(1,3)
  args['scatter'] = False
  args['vol'] = 100
  return args



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  args = parser.parse_args()
  debug = args.debug
  hostList = host.getHosts()
  screenList = []
  phraseList = []
  for h in hostList:
    if h['hasScreen']:
      if host.sendToHost(h['ip'],{'cmd' : 'Probe', 'args' : [""] }):
        screenList.append(h)
        if debug: print "adding",h
      else:
        print "skipping:",h
    if h['hasAudio']:
      if host.sendToHost(h['ip'],{'cmd' : 'Probe', 'args' : [""] }):
        phraseList.append(h)
        if debug: print "adding",h
  while True:
    for h in screenList:
      args = getPhrase()
      if debug: print "Show args:",args
      host.sendToHost(h['ip'],{'cmd' : 'Show', 'args' : args })
    h = random.choice(phraseList)
    args = getPhrase()
    args = setPhraseParms(args)
    if debug: print "Phrase args:",args
    host.sendToHost(h['ip'],{'cmd' : 'Phrase', 'args' : args })
    time.sleep(random.randint(5,10))

