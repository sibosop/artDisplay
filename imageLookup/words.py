#!/usr/bin/env python
import adGlobal
import random

debug=False

class Words:
  
  lines = []
  wordList = None
  wordDir = None

  def __init__(self):
    self.wordList = adGlobal.wordList
    self.wordDir= adGlobal.wordDir
    for w in self.wordList:
      f = open(self.wordDir+"/"+w,"r")
      for l in f.read().split('\n'):
        self.lines.append(l)
    
    #self.lines = open(self.wordFile).read().split('\n')

  def getWords(self):
    tests=[]
    for i in range(0,2):
      n = random.randint(0,len(self.lines)-1)
      tests.append(self.lines[n])
    if debug: print "tests:",tests[0],tests[1] #,tests[2]
    return tests

if __name__ == '__main__':
  w=Words()
  choices = w.getWords()
  print choices
