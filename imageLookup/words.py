#!/usr/bin/env python
import adGlobal
import random
import time

debug=False

lines = []
wordList = None
wordDir = None
global init
init=False


def initWords():
  if debug: print "init words"
  random.seed(time.time())
  wordList = adGlobal.wordList
  wordDir= adGlobal.wordDir
  for w in wordList:
    f = open(wordDir+"/"+w,"r")
    for l in f.read().split('\n'):
      lines.append(l)
  init=True


#@profile
def getWords():
  global init
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
  choices = getWords()
  choices = getWords()
  choices = getWords()
  print choices
