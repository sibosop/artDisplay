#!/usr/bin/env python
import syslog
import os
import sys
from subprocess import CalledProcessError, check_output
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import adGlobal
debug=True
micKey="MIC_CARD"
speakerKey="SPEAKER_CARD"

usbMic="USB-Audio - USB PnP Sound Device"
usbSpeaker="USB-Audio - USB2.0 Device"
usbSpeakerAlt="USB-Audio - USB Audio Device"


def getCardNum(line,key):
  rval=""
  if line.find(key) != -1:
    if debug: syslog.syslog("found "+key+":"+line)
    rval = line.split()[0].strip()
  return rval

hwInit = False
hw={}
def setSpeakerInfo(hw):
  cmdHdr = ["amixer", "-c",hw['Speaker']]
  try:
    cmd = cmdHdr[:]
    output = check_output(cmd)
    lines = output.split("\n");
    for l in lines:
      n = l.find("Limits: Playback") 
      if n != -1:
        vars = l.split()
        hw['min'] = vars[2]
        hw['max'] = vars[4]

  except CalledProcessError as e:
    syslog.syslog(e.output)



def getHw():
  global hwInit
  global hw
  if hwInit is False:
    hw['Mic']="0"
    hw['Speaker']=0
    cardPath = "/proc/asound/cards"
    with open(cardPath) as f:
      for line in f:
        t = getCardNum(line,usbMic)
        if t != "":
          hw['Mic'] = t
        t = getCardNum(line,usbSpeaker)
        if t != "":
          hw['Speaker'] = t
          hw['SpeakerBrand']= "HONK"
        t = getCardNum(line,usbSpeakerAlt)
        if t != "":
          hw['Speaker'] = t
          hw['SpeakerBrand'] = "JLAB"

    #retrieve info about speaker
    setSpeakerInfo(hw)
    hwInit = True
  return hw 
  

def makeRc():
  path = adGlobal.sharedDir+"/asoundrc.template"
  rcPath = home+"/.asoundrc"
  try:
    if debug: syslog.syslog("HOME="+home+" Prog="+adGlobal.progDir)
    rc = open(rcPath,"w")
    hw = getHw()
    with open(path) as f:
      for line in f:
        if line.find(micKey) != -1:
          line = line.replace(micKey,hw['Mic'])
        elif line.find(speakerKey) != -1:
          line = line.replace(speakerKey,hw['Speaker'])
        rc.write(line)
  except Exception, e:
    syslog.syslog("player error: "+repr(e))

# amixer -c 2 cset numid=3,name='PCM Playback Volume' 100
def setVolume(vol):
  if int(vol) >= 100 :
    vol = "100"
  hw=getHw()
  syslog.syslog("max volume:"+hw['max'])
  volRat = int(hw['max'])/100.0
  setVol = float(vol) * volRat
  setVol = int(setVol)
  syslog.syslog("max volume:"
    +hw['max']
    +" Rat:"
    +str(volRat)
    +" Vol:"
    +str(vol)
    +" SetVol:"
    +str(setVol)
    )
  cmdHdr = ["amixer", "-c",hw['Speaker']]
  try:
    cmd = cmdHdr[:]
    cmd.append("controls")
    output = check_output(cmd)
    lines = output.split("\n");
    for l in lines:
      if l.find("Volume") != -1:
        vars = l.split(",")
        cmd = cmdHdr[:]
        cmd.append("cset")  
        cmd.append(vars[0]+","+vars[2])
        cmd.append(str(setVol)) 
        if debug: syslog.syslog("vol:"+str(cmd))
        output = check_output(cmd)

  except CalledProcessError as e:
    syslog.syslog(e.output)


if __name__ == '__main__':
  makeRc()
  #setVolume(sys.argv[1])

