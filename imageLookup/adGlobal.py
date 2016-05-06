#!/usr/bin/env python
import platform
import os
import syslog

home="/home/pi"

plats=platform.platform().split('-');
if plats[0] == 'Darwin':
  home="/Users/brian"

cacheDir=home+"/ImageCache"
wordFile=home+"/GitProjects/artDisplay/imageLookup/corncob_lowercase.txt"
binDir=home+"/GitProjects/artDisplay/imageChecker"
panelDev="/dev/ttyUSB0"

def getCacheDir():
  if not os.path.exists(cacheDir):
    syslog.syslog(syslog.LOG_ERR,"Cache Directory "+cacheDir+" does not exist")
    exit(-1)
  return cacheDir
