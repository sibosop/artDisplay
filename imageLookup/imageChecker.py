#!/usr/bin/env python
import os
import subprocess
import time
import psutil
import adGlobal
import syslog

debug = False
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
  syslog.syslog("calling feh with "+img);
  p = subprocess.Popen("feh -Z -F "+img,shell=True)
  time.sleep(4)
  if currentProc is not None:
    if debug:
      print "kill ",currentProc
    kill(currentProc.pid)
    
  currentProc = p
  currentImg=img
  os.unlink(currentImg)
  return None

def getImage():
  filenames = next(os.walk(imageDir))[2]
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
      delFile = imageDir+'/'+f
      os.unlink(delFile)
      root = f[:ext]
      for se in imageExts:
        look=imageDir+'/'+root+se;
        if debug:
          print "looking for",look
        if os.path.exists(look):
          return look
  return None

def imageChecker():
  os.environ["DISPLAY"] = ":0.0"
  global imageDir
  imageDir = adGlobal.imageDir
  if debug:
    print "image image dir:",imageDir
  count=0
  syslog.syslog("image checker started successfully")
  while True:
    if debug:
      count += 1
      print "checking for image. count:",count
    img = getImage();
    if img is None:
      if debug:
        print "no image"
    else:
      if debug:
        print "found image",img
      displayImage(img)
    time.sleep(5)
  
    

if __name__ == '__main__':
  imageChecker()

  