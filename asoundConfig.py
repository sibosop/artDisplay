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

micNum = "1"
speakerNum = "2"

def main():
  cardPath = "/proc/asound/cards"
  path = adGlobal.progDir+"/asoundrc.template"
  rcPath = home+".asoundrc"
  try:
    if debug: syslog.syslog("HOME="+home+" Prog="+adGlobal.progDir)
    with open(path) as f:
      for line in f:
        line = line.rstrip()
        if line.find(micKey) != -1:
          line = line.replace(micKey,micNum)
        elif line.find(speakerKey) != -1:
          line = line.replace(speakerKey,speakerNum)
        print line
  except Exception, e:
    syslog.syslog("player error: "+repr(e))


main()

