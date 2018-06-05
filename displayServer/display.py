#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
import syslog
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
sys.path.append(home+"/GitProjects/artDisplay/poem")
import slp
import master
import syslog
import datetime
import time
import adGlobal
import displayServer
import pygame

debug = False
schlubExit = 0
attr=""


if __name__ == '__main__':
  adGlobal.hasAudio=True
  pname = sys.argv[0]
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  syslog.syslog(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  
  pygame.init()
  slp.start()
  im = master.isMaster()
  slp.register("display",attr)
  sst = displayServer.displayServerThread(8080)
  sst.setDaemon(True)
  sst.start()
  while schlubExit == 0:
    try:
      time.sleep(5)
    except KeyboardInterrupt:
      syslog.syslog(pname+": keyboard interrupt")
      break
    except Exception as e:
      syslog.syslog(pname+":"+str(e))
      break

  syslog.syslog(pname+" exiting")
  exit(schlubExit)

