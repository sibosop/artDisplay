#!/usr/bin/env python
import platform
import os
import syslog
import subprocess
import urllib2
from threading import Lock
mutex = Lock()

debug=False
home="/home/pi"
imageDir='../Images'
cacheDir="../ImageCache"
fontDir="../fonts"
imageDest="GitProjects/artDisplay/imageLookup/"+imageDir
defaultImg="./splash.jpg"
bingFile="./corncob_lowercase.txt"
wordDir="../lists"
wordList=["corncob_lowercase.txt"]
panelDev="/dev/ttyUSB0"
#searchType="Google"
#searchType="Bing"
searchType="Archive"
doArchive=True
archiveDir='/media/pi/ARCHIVE/ArchiveImages/'
archiveCache='../archiveCache'
textName='newText.lkp'
credFile='/media/pi/ARCHIVE/creds.txt'
timeStampFile = '/tmp/adTimeStamp'
lineSpacing = 20
voiceDir="../tmp"
subnet="10"

def internetOn():
  try:
    urllib2.urlopen('http://216.58.192.142', timeout=1)
    return True
  except urllib2.URLError as err: 
    return False
  
def isLocalHost(ip):
  plats=platform.platform().split('-');
  if plats[0] == 'Darwin':
    return False
  myIp = subprocess.check_output(["hostname","-I"]).split()
  for i in myIp:
    if debug: syslog.syslog("isLocalHost: ip:"+ip+ " myIp:"+i)
    if i == ip:
      if debug: syslog.syslog("isLocalHost is True:"+ip)
      return True
  if debug: syslog.syslog("isLocalHost is False:"+ip)
  return False
