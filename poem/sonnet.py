#!/usr/bin/env python
import roman
import syslog
import random
debug = True

def get(author,maxSonnet,textFile):
  choice = random.randint(1,maxSonnet)
  if debug: syslog.syslog("Get Sonnet:"+str(choice))

  found=False
  sonnet = []
 
  with open(textFile) as f:
    for line in f:
      if found:
        l = line.strip()
        if len(l) == 0:
          if len(sonnet) != 0:
            l = author + " Sonnet "+str(choice)
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
