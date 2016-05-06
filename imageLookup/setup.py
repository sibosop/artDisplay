#!/usr/bin/env python
import subprocess
import syslog
import threading
import textChecker
import master
import sys
import imageLookup
import imageChecker
import os

debug = True
if __name__ == '__main__':

  host = subprocess.check_output(["hostname","-I"]).split();
  if debug:
    syslog.syslog("host ="+host[0])
    
  test = subprocess.check_call(["sudo","service","slpd","start"])
  test = subprocess.check_call(["slptool","register","service:artdisplay.x://"+host[0]])
  try:
    os.environ["DISPLAY"] = ":0.0"
    tc = threading.Thread(target=textChecker.textChecker)
    tc.setDaemon(True)
    tc.start()
    
    im = master.isMaster()
    ti = threading.Thread(target=imageLookup.imageLookup)
    ti.setDaemon(True)
    if im:
      ti.start()  
    tic = threading.Thread(target=imageChecker.imageChecker)
    tic.setDaemon(True)
    tic.start()
    while True:
      tc.join(1)  
      if im:
        ti.join(1)
      tic.join(1)
  except:
    e = sys.exc_info()[0]
    syslog.syslog("return from exception "+str(e))