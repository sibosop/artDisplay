#!/usr/bin/env python
import subprocess
import syslog

debug = True
if __name__ == '__main__':

  host = subprocess.check_output(["hostname","-I"]).split();
  if debug:
    syslog.syslog("host ="+host[0])
    
  test = subprocess.check_call(["sudo","service","slpd","start"])
  test = subprocess.check_call(["slptool","register","service:artdisplay.x://"+host[0]])
