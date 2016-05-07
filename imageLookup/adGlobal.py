#!/usr/bin/env python
import platform
import os
import syslog
import subprocess

debug=True
home="/home/pi"
imageRoot='../Images'
cacheDir="../ImageCache"
imageDest="GitProjects/artdisplay/imageLookup/"+"imageRoot"
wordFile="./corncob_lowercase.txt"
panelDev="/dev/ttyUSB0"

  
def isLocalHost(ip):
  plats=platform.platform().split('-');
  if plats[0] == 'Darwin':
    return False
  myip = subprocess.check_output([hostname,-I]).split()[0]
  if debug: print "ip:",ip
  if debug: print "myip:",myip
  return myIp == ip