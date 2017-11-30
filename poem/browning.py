#!/usr/bin/env python
import sonnet
author="Elizabeth Barrett Browning"

max = 44
#max = 2
textFile = "browning.txt"

def getId():
  return "browning"

def getNumPoems():
  return max

def getMinPoem():
  return 1
def create(choice):
  return sonnet.get(author,choice,textFile)
