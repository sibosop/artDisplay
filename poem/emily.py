#!/usr/bin/env python
import roman
import sys
import syslog
import random
import re
import fileDecoder

debug = False

def emilySectionRe():
  return re.compile('^[IVXLCDM]+\.\s+.+\.$')

def emilyRe():
  return re.compile('^[IVXLCDM]+\.$')

def get():
  series = 0
  pcount = 0
  maxPoem = 448
  poem = ["Emily Dickenson"]
  choice = random.randint(1,maxPoem)
  found = False
  title = ""
  section = ""
  fd = fileDecoder.fileDecoder("emily.txt")
  while True:
    line = fd.next()
    if line is None:
      break
    if line == "":
      continue
    if debug: syslog.syslog("raw line:"+line)
    test = roman.roman_to_int(line,emilySectionRe)
    if test != 0:
      section = test
      test = line.strip()
      test = test[test.find(" "):].lstrip().replace(".","")
      if test == "LIFE":
        series += 1
      title = test
      if debug: syslog.syslog("found series:"+str(series)
                  +" section:"+str(section)
                  +" title:"+title)
      continue
    if found:
      test = roman.roman_to_int(line,emilyRe)
      if test != 0:
        break
      poem.append(line)
      if line.isupper():
        poem.append("+++++")
    else:
      test = roman.roman_to_int(line,emilyRe)
      if debug: syslog.syslog("roman int:"+str(test))
      if test != 0:
        pcount += 1
        if pcount == choice:
          if debug: syslog.syslog( "found: "+ str(choice))
          poem.append("Number: " + str(test))
          poem.append("Series: "+  str(series))
          poem.append("Subject: " + title)
          poem.append("+++++")
          found = True

  return poem

if __name__ == '__main__':
  poem = get()
  for l in poem:
    print l
