#!/usr/bin/env python
import sys
import os
import syslog
import subprocess
import threading
import textChecker
import master
import imageLookup
import imageChecker
import panel
import time
import datetime

if __name__ == '__main__':
  sys.stderr.write("art display at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"\n")
  debug = False
  os.chdir(os.path.dirname(sys.argv[0]))
  sys.stderr.write("starting setup.py"+"\n")
  host = subprocess.check_output(["hostname","-I"]).split();
  if debug:
    sys.stderr.write("host ="+host[0]+"\n")
    
  test = subprocess.check_call(["sudo","service","slpd","start"])
  regs=["slptool","register","service:artdisplay.x://"+host[0]]
  hp=panel.hasPanel()
  if hp:
    regs.append("hasPanel=true")
  test = subprocess.check_call(regs)

  try:
    os.environ["DISPLAY"] = ":0.0"
    tc = threading.Thread(target=textChecker.textChecker)
    tc.setDaemon(True)
    
    if hp:
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
      if hp:
        tc.join(1)  
      if im:
        ti.join(1)
      tic.join(1)
  except:
    e = sys.exc_info()[0]
    sys.stderr.write("return from exception "+str(e)+"\n")
