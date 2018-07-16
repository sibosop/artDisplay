#!/usr/bin/env python
import sys
import os
import time
import host
import json
import argparse
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/config")
sys.path.append(home+"/GitProjects/artDisplay/bottery")
import config
import dataio


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
  rval = phrase
  return rval

langs=["en", "en-au", "en-uk" ]

def setPhraseParms(args):
  args['lang'] = random.choice(langs)
  args['reps'] = random.randint(1,3)
  args['scatter'] = False
  args['vol'] = 100
  return args

wsCmd = ['nw','rw','cc','ph']
def getWordServerCommand():
  rval = random.choice(wsCmd) + "?n=" + str(random.randint(1,5))
  if debug: print "word server command:",rval
  return rval
  

def defaultPhrase():
  return getPhrase()

rel_codes = ['ml','rel_syn','rel_ant','rel_trg','rel_jjb'] 

def doDataMuse(w):
  rval = w + " "
  dcmd = random.choice(rel_codes)
  t = dataio.datamuse(w,dcmd)
  if debug: print "w:",w,"datamuse:",t,"dcmd:",dcmd
  if len(t) != 0:
    s = random.choice(t)
    rval += s[0] + " "
  return rval

if __name__ == '__main__':
  if config.specs == None:
    config.load()
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  parser.add_argument('-p','--parrot', nargs='?',help='set parrot name',default=config.specs['parrotName'])
  args = parser.parse_args()
  debug = args.debug
  hostList = host.getHosts()
  screenList = []
  phraseList = []
  myParrot = None
  for h in hostList:
    if h['hasScreen']:
      screenList.append(h)
      if debug: print "adding",h
    if h['hasAudio']:
      phraseList.append(h)
      if debug: print "adding",h
    if h['hasParrot']:
      if h['name'] == args.parrot:
        myParrot = h
   
  while True:
    if myParrot == None:
      defaultSend()
    else:
      cmd = random.choice(wsCmd)
      n = 1
      if cmd != 'ph':
        n = random.randint(1,5)
      send = cmd + "?n="+str(n)
      rval = json.loads(host.sendToWordServer(myParrot['ip'],send))
      if debug: print "send to word server for cmd:",cmd,"returns",rval
      if rval['status'] == 200:
        phrase = ""
        if cmd == "nw" or cmd == "rw":
          if random.randint(0,1):
            for w in rval['data']:
              phrase += w[0] + " " 
          else:
            for w in rval['data']:
              phrase += doDataMuse(w[0])
        elif cmd=="cc":
          if random.randint(0,1):
            for w in rval['data']:
              phrase += doDataMuse(w)
          else:
            for w in rval['data']:
              phrase += w + " "
        elif cmd == "ph":
          phrase = rval['data'][0][0]
        else:
          if debug: print "cmd not supported:",cmd
          phrase = defaultPhrase()
      else:
        if debug: print "server error:", rval['status']
        phrase = defaultPhrase()
        
      if debug: print "chosen phrase:", phrase
      args = {}
      args['phrase'] = phrase
      if random.randint(0,1):
        args = setPhraseParms(args)
        h = random.choice(phraseList)
        if debug: print "send phrase:", args,"ip",h['ip']
        host.sendToHost(h['ip'],{'cmd' : 'Phrase', 'args' : args })
      else:
        h = random.choice(screenList)
        if debug: print "show phrase:", args,"ip",h['ip']
        host.sendToHost(h['ip'],{'cmd' : 'Show', 'args' : args }) 
        
      
        
    time.sleep(random.randint(5,10))

