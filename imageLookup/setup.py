#!/usr/bin/env python
import sys
import os
import syslog
syslog.syslog("starting setup.py")
import subprocess
import threading
syslog.syslog("import textChecker.py")
import textChecker
syslog.syslog("import master.py")
import master
syslog.syslog("import imageLookup.py")
import imageLookup
syslog.syslog("import imageChecker.py")
import imageChecker
syslog.syslog("import panel.py")
import panel

if __name__ == '__main__':
  debug = False
  os.chdir(os.path.dirname(sys.argv[0]))
  syslog.syslog("starting setup.py")
  host = subprocess.check_output(["hostname","-I"]).split();
  if debug:
    syslog.syslog("host ="+host[0])
    
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
    syslog.syslog("return from exception "+str(e))
