#!/usr/bin/env python
import os
import subprocess
import time
import psutil

debug = True
cacheDir = None
flagExt=".flg"
currentProc = None
currentImg = None

imageExts=['.jpg','.png','.jpeg']

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def displayImage(img):
  global currentProc
  global currentImg
  if debug:
    print "display ",img
  p = subprocess.Popen("feh -F "+img,shell=True)
  time.sleep(4)
  if currentProc is not None:
    if debug:
      print "kill ",currentProc
    kill(currentProc.pid)
    os.unlink(currentImg)
  currentProc = p
  currentImg=img
  return None

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
      delFile = cacheDir+'/'+f
      os.unlink(delFile)
      root = f[:ext]
      for se in imageExts:
        look=cacheDir+'/'+root+se;
        if debug:
          print "looking for",look
        if os.path.exists(look):
          return look
  return None


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
      displayImage(img)
    time.sleep(5)
  
    
  