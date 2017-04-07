#!/usr/bin/env python
import roman
import syslog
import random
import fileDecoder
debug = True

def get(author,maxSonnet,textFile):
  choice = random.randint(1,maxSonnet)
  if debug: syslog.syslog("Get Sonnet:"+str(choice))

  found=False
  sonnet = []
  fd = fileDecoder.fileDecoder(textFile)
  while True:
    line = fd.next()
    if line is None:
      break

    if found:
      if len(line) == 0:
        if len(sonnet) != 0:
          l = author + " Sonnet "+str(choice)
          sonnet.insert(0,l)
          sonnet.insert(1,"+++++")
          return (sonnet)
      else:
        sonnet.append(line)
    else:
      test = roman.roman_to_int(line)
      if test==choice:
        found = True

  return None
