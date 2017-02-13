#!/usr/bin/env python
import os
import subprocess
import time
import psutil
import adGlobal
import syslog
import signal
import sys
import inspect
debug = False
flagExt=".flg"
currentProc = None
currentImg = None
timestamp = 0;

hangDebug=True;



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
  #syslog.syslog("calling feh with "+img);
  try:
    if hangDebug: syslog.syslog("Hang debug:"
		+__file__+" "
		+str(inspect.currentframe().f_lineno))
    p = subprocess.Popen("/usr/bin/feh -Z -F "+img,shell=True, preexec_fn=os.setpgrp)
  except:
    e = sys.exc_info()[0]
    print "return from exception "+str(e)
    return None
  time.sleep(4)
  if currentProc is not None:
    if debug:
      print "kill ",os.getpgid(currentProc.pid)
    if hangDebug: syslog.syslog("Hang debug:"
		+__file__+" "
		+str(inspect.currentframe().f_lineno))
    os.killpg(os.getpgid(currentProc.pid), signal.SIGTERM) 
    
  currentProc = p
  currentImg=img
  if hangDebug: syslog.syslog("Hang debug:"
	+__file__+" "
	+str(inspect.currentframe().f_lineno))
  adGlobal.mutex.acquire()
  if hangDebug: syslog.syslog("Hang debug:"
		+__file__+" "
		+str(inspect.currentframe().f_lineno))
  os.unlink(currentImg)
  if hangDebug: syslog.syslog("Hang debug:"
		+__file__+" "
		+str(inspect.currentframe().f_lineno))
  adGlobal.mutex.release()
  return None

def getImage():
  global timestamp;
  stampFile = adGlobal.timeStampFile;
  if os.path.isfile(stampFile):
    adGlobal.mutex.acquire()
    timestamp = os.path.getmtime(stampFile)
    adGlobal.mutex.release()
  adGlobal.mutex.acquire()
  filenames = next(os.walk(imageDir))[2]
  adGlobal.mutex.release()
  for f in filenames:
    if debug:
      syslog.syslog("filename:"+f)
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
      adGlobal.mutex.acquire()
      flagTimeStamp = os.path.getctime(delFile);
      os.unlink(delFile)
      adGlobal.mutex.release()
      root = f[:ext]
      for se in imageExts:
        look=imageDir+'/'+root+se;
        if os.path.exists(look):
          if debug:
            syslog.syslog("look:"
                +look
                + " flagTimeStamp:"
                + str(flagTimeStamp)
                + " timestamp:"+str(timestamp))
          if flagTimeStamp < timestamp:
            syslog.syslog("deleting out of date image:"+look);
            adGlobal.mutex.acquire()
            os.unlink(look)
            adGlobal.mutex.release()
          else:
            syslog.syslog("returning for display: "+look);
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
  try:
    p = subprocess.Popen("/usr/bin/feh -Z -F "+adGlobal.defaultImg,shell=True, preexec_fn=os.setpgrp)
  except:
    e = sys.exc_info()[0]
    print "return from exception "+str(e)
    return None
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

  
