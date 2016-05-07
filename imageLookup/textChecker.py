#!/usr/bin/env python

import os
import time
import adGlobal
import panel
import syslog
debug = False


      
textExt = ".lkp"
def getText():
  filenames = next(os.walk( imageDir))[2]
  for f in filenames:
    if debug:
      print "filename:",f
    try:
      ext = f.rindex(textExt)
    except ValueError:
      if debug:
        print "not lookup text file"
      continue
    flag = f[ext:]
    if flag == textExt:  
      if debug:
        print "found text file",f
      path =  imageDir + "/" + f
      lines = open(path).read().split('\n')
      if len(lines) > 1:
        os.unlink(path)
        return lines
      
  return None

def textChecker():
  if not panel.setUpPanel():
    syslog.syslog("exiting")
    return
    
  global  imageDir
   imageDir=adGlobal.getImageDir()

  
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
