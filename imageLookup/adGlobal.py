#!/usr/bin/env python
import platform
import os
import syslog
import subprocess

debug=False
home="/home/pi"
imageDir='../Images'
cacheDir="../ImageCache"
imageDest="GitProjects/artDisplay/imageLookup/"+imageDir
wordFile="./corncob_lowercase.txt"
#wordFile="./words.txt"
panelDev="/dev/ttyUSB0"

  
def isLocalHost(ip):
  plats=platform.platform().split('-');
  if plats[0] == 'Darwin':
    return False
  myIp = subprocess.check_output(["hostname","-I"]).split()[0]
  if debug: print "ip:",ip
  if debug: print "myIp:",myIp
  return myIp == ip
