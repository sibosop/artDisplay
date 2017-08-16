#!/usr/bin/env python
import sonnet
author="Elizabeth Barrett Browning"
max = 44
textFile = "browning.txt"

def get():
  return sonnet.get(author,max,textFile)
