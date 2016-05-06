#!/usr/bin/env python
import subprocess
import syslog
import threading
import  textChecker

debug = True
if __name__ == '__main__':

  host = subprocess.check_output(["hostname","-I"]).split();
  if debug:
    syslog.syslog("host ="+host[0])
    
  test = subprocess.check_call(["sudo","service","slpd","start"])
  test = subprocess.check_call(["slptool","register","service:artdisplay.x://"+host[0]])
  try:
    tc = threading.Thread(target=textChecker.textChecker)
    tc.setDaemon(True)
    tc.start()
    while True:
      tc.join(1)
  except:
    syslog.syslog("return from exception")