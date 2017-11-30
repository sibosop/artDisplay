#!/usr/bin/env python
import os
import sonnet
import mkPoemData
author="Shakespeare"
max = 154
#max=3
textFile = "wssnt10.txt"

def getId():
  return author

def getMinPoem():
  return 1

def getNumPoems():
  return max

def create(num):
  print "get sonnet:",num
  data = sonnet.get(author,num,textFile)
  return data



    
  
