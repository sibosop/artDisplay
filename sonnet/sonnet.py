#!/usr/bin/env python
import syslog
import time
import random
import re
import displayText

debug = False
numeral_map = None

def roman_to_int(n):
  n = n.strip()

  reg=re.compile('^[IVXLCDM]+$')
  if reg.match(n) is None:
    #syslog.syslog(n+": not a match")
    return 0
  i = result = 0
  for integer, numeral in numeral_map:
    while n[i:i + len(numeral)] == numeral:
      result += integer
      i += len(numeral)
  return result

def getSonnet():
  global numeral_map
  if numeral_map is None:
    numeral_map = zip(
      (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
      ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    )
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
            l = "Sonnet number "+str(choice)
            sonnet.insert(0,l)
            return (sonnet)
        else:
          sonnet.append(l)
      else:
        test = roman_to_int(line)
        if test==choice:
          if debug: syslog.syslog(line+":"+str(test))
          found = True

  return None
  

if __name__ == '__main__':
  while True:
    for l in getSonnet():
      if debug: syslog.syslog(l)
      displayText.displayText(l)
      time.sleep(5)
