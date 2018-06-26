#!/usr/bin/env python
import wikipedia
import sys
import random
import schlubcmd
import re
import os

if __name__ == '__main__':
  pos = 0
  for a in sys.argv:
    print "a:",a
    if a == "search":
      args = sys.argv[pos+1:]
      break
    else:
      pos += 1
  sys.argv = sys.argv[0:pos]
  schlubcmd.getHostList()
  schlubcmd.printHostList()
  print args
  query = ""
  for a in args:
    query += a + " "
  try:
    words = wikipedia.page(query).content.split()
  except:
    print "bad term"
    os._exit(-1)
  print "num words:",len(words)
  phrase = ""
  count = 0
  while count < 3:
    choice = random.choice(words)
    if len(choice) < 5:
      continue
    phrase += re.sub(r'\W+', '', choice) + " "
    count += 1

  print phrase
  reps = 1
  vol = 100
  args = {}
  args['phrase'] = phrase
  args['reps'] = reps
  args['scatter'] = False
  args['lang'] = 'en-uk'
  args['vol'] = vol
  schlubcmd.sendToHosts({'cmd' : "Phrase", 'args' : args})
    
  

