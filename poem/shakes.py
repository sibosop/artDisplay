#!/usr/bin/env python
import sonnet
author="Shakespeare"
max = 154
textFile = "wssnt10.txt"

def get():
  return sonnet.get(author,max,textFile)
