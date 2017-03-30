#!/usr/bin/env python
import roman
import syslog
import random
debug = True

def get():
  maxSonnet=154
  choice = random.randint(1,154)
  if debug: syslog.syslog("Get Sonnet:"+str(choice))

  found=False
  sonnet = []
 
  with open("wssnt10.txt") as f:
    for line in f:
      if found:
        l = line.strip()
        if len(l) == 0:
          if len(sonnet) != 0:
            l = "Shakespeare Sonnet "+str(choice)
            sonnet.insert(0,l)
            sonnet.insert(1,"+++++")
            return (sonnet)
        else:
          sonnet.append(l)
      else:
        test = roman.roman_to_int(line)
        if test==choice:
          if debug: syslog.syslog(line+":"+str(test))
          found = True

  return None
