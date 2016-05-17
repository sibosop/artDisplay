#!/usr/bin/env python

import adGlobal
import glob
import random
import subprocess
import os

debug=True

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
    cmd=["tar","xzf",adir+"/"+archives[n],"-C",cdir]
    if debug: print "cmd:",cmd
    subprocess.check_output(cmd)
  except subprocess.CalledProcessError, e:
    syslog.syslog("archive problem: "+', '.join(cmd)+str(e.output))
    

if __name__ == '__main__':
  getArchive()