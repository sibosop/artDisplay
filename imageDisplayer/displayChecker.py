#!/usr/bin/env python
import os
import subprocess
import time

debug = True
cacheDir = None
flagExt=".flg"

imageExts=['.jpg','.png','.jpeg']

def getImage():
  filenames = next(os.walk(cacheDir))[2]
  for f in filenames:
    if debug:
      print "filename:",f
    try:
      ext = f.rindex(flagExt)
    except ValueError:
      if debug:
        print "not flag file"
      continue
    flag = f[ext:]
    if debug:
      print"flag ext = ",flag
    if flag == flagExt:
      root = f[:ext]
      for se in imageExts:
        look=cacheDir+'/'+root+se;
        if debug:
          print "looking for",look
        if os.path.exists(look):
          return look
          
    
  return None;


if __name__ == '__main__':
  print "hello world"
  cacheDir = os.environ.get('ID_CACHE');
  if cacheDir is None:
    print "Error: ID_CACHE not defined"
    exit(-1)

  print "image cache dir:",cacheDir
  if not os.path.exists(cacheDir):
    print "Error: chacheDir",cacheDir,"does not exist"
    exit(-1)
    
  while True:
    if debug:
      print "checking for image"
    img = getImage();
    if img is None:
      if debug:
        print "no image"
    else:
      if debug:
        print "found image",img
    time.sleep(5)
  
    
  