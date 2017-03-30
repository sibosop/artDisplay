#!/usr/bin/env python
import roman
import sys
import syslog
import random
import re

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
  with open("emily.txt") as f:
    for line in f:
      line = line.strip()
      if not line:
        continue
      test = roman.roman_to_int(line,emilySectionRe)
      if test != 0:
        section = test
        test = line.strip()
        test = test[test.find(" "):].lstrip().replace(".","")
        if test == "LIFE":
          series += 1
        title = test
        if debug: syslog.syslog("found series:"+series+"section:"+section+"title:"+title)
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
        if test != 0:
          pcount += 1
          if pcount == choice:
            if debug: syslog.syslog( "found: "+ choice )
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
