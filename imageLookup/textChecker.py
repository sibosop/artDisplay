#!/usr/bin/env python

import os
import time
import adGlobal
import panel
import syslog
import sys
debug = False


      
textExt = ".lkp"
def getText():
  filenames = next(os.walk( adGlobal.imageDir))[2]
  for f in filenames:
    if debug:
      syslog.syslog( "filename:"+f )
    try:
      ext = f.rindex(textExt)
    except ValueError:
      if debug:
        syslog.syslog( "not lookup text file" )
      continue
    flag = f[ext:]
    if flag == textExt:  
      if debug:
          syslog.syslog("found text file:"+f)
      path =  adGlobal.imageDir + "/" + f
      lines = open(path).read().split('\n')
      if len(lines) > 1:
        adGlobal.mutex.acquire()
        os.unlink(path)
        adGlobal.mutex.release()
        return lines
      
  return None

def textChecker():
  if not panel.setUpPanel():
    syslog.syslog("exiting")
    return
    
  
  count=0
  syslog.syslog("text checker started successfully")
  while True:
    if debug:
      count += 1
      print "checking for text. count:",count
    text = getText();
    if text == None:
      if debug:
        print "no text"
    else:
      if debug:
        print "found test",text
      panel.printText(text)
    time.sleep(5)
    
if __name__ == '__main__':
  textChecker()
