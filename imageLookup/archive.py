#!/usr/bin/env python

import adGlobal
import glob
import random
import subprocess
import os
import sys
import syslog

debug=False

def getArchive():
  adir=adGlobal.archiveDir
  cdir=adGlobal.archiveCache
  files = glob.glob(cdir+"/*")
  if debug: print "removing:",files
  for f in files:
    if f == cdir+"/placeholder":
      continue
    os.remove(f)
    
  archives=[]
  for a in glob.glob(adir+"/*.tgz"):
    if debug: print "a:",a
    archives.append(a)
  n = random.randint(0,len(archives)-1)
  if debug: print "archive choice",archives[n]
  try:  
    cmd=["tar","xzf",archives[n],"-C",cdir]
    if debug: print "cmd:",cmd
    subprocess.check_output(cmd)
  except subprocess.CalledProcessError, e:
    syslog.syslog("archive problem: "+', '.join(cmd)+str(e.output))
  images=[]
  choices=[]
  try:
    for a in glob.glob(cdir+"/*.jpg"):
      if debug: print "archive image",a
      images.append(a);
  except:
    e = sys.exc_info()[0]
    syslog.syslog("return from archive image append "+str(e))
  
  textName=cdir+"/"+adGlobal.textName
  if debug: print "textName",textName  
  try:  
    with open(textName) as fp:
        for line in fp:
            if debug: print line.rstrip()
            choices.append(line.rstrip())
  except:
    e = sys.exc_info()[0]
    syslog.syslog("choice name append "+str(e))
  return [images,choices]
  
    

if __name__ == '__main__':
  rval=getArchive()
  images=rval[0]
  choices=rval[1]
  for i in images:
    print i
  for i in choices:
    print i