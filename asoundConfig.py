#!/usr/bin/env python
import syslog
import os
import sys
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import adGlobal
debug=True
micKey="MIC_CARD"
speakerKey="SPEAKER_CARD"

usbMic="USB-Audio - USB PnP Sound Device"
usbSpeaker="USB-Audio - USB2.0 Device"

micNum = "1"
speakerNum = "2"

def getCardNum(line,key):
  rval=""
  if line.find(key) != -1:
    if debug: syslog.syslog("found "+key+":"+line)
    rval = line.split()[0].strip()
  return rval
  

def main():
  global micNum
  global speakerNum
  cardPath = "/proc/asound/cards"
  path = adGlobal.progDir+"/asoundrc.template"
  rcPath = home+"/.asoundrc"
  try:
    if debug: syslog.syslog("HOME="+home+" Prog="+adGlobal.progDir)
    with open(cardPath) as f:
      for line in f:
        t = getCardNum(line,usbMic)
        if t != "":
          micNum = t
        t = getCardNum(line,usbSpeaker)
        if t != "":
          speakerNum = t
    rc = open(rcPath,"w")
    with open(path) as f:
      for line in f:
        if line.find(micKey) != -1:
          line = line.replace(micKey,micNum)
        elif line.find(speakerKey) != -1:
          line = line.replace(speakerKey,speakerNum)
        rc.write(line)
  except Exception, e:
    syslog.syslog("player error: "+repr(e))


main()

