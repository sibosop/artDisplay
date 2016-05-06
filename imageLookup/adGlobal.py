#!/usr/bin/env python
import os
import syslog

homeDir="/home/pi"
binDir=homeDir+"GitProjects/artDisplay/imageChecker"
cacheDir=homeDir+"/ImageCache"
panelDev="/dev/ttyUSB0"

def getCacheDir():
  if not os.path.exists(cacheDir):
    syslog.syslog(syslog.LOG_ERR,"Cache Directory "+cacheDir+" does not exist")
    exit(-1)
  return cacheDir
