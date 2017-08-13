#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
import syslog
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import slp
import master
import syslog
import datetime
import time
import adGlobal
import threading
import phraseLookup

if __name__ == '__main__':
  adGlobal.hasAudio=True
  pname = sys.argv[0]
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  syslog.syslog(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  slp.start()
  slp.register("phrase","")

  pt = phraseLookup.phraseLookupThread()
  pt.setDaemon(True)
  pt.start()
  while True:
    try:
      time.sleep(5)
    except KeyboardInterrupt:
      syslog.syslog(pname+": keyboard interrupt")
      break
    except Exception as e:
      syslog.syslog(pname+":"+str(e))
      break



