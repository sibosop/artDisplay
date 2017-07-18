#!/usr/bin/env python
import subprocess
import urllib
import os
home = os.environ['HOME']
import sys
import slp
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import adGlobal

debug=True

hosts = []


def printHostList():
  print "Host list:"
  for h in hosts:
    o = h['ip']
    if 'attr' in h:
      if debug: print "attr",h['attr']
      o += " "+h['attr']
    print " ",o
  print

def printCmds():
  print "SchlubCmds:"

  print " auto - set auto play mode"
  print " hosts - print host list"
  print " manual - set manual play mode"
  print " off - power off hosts"
  print " play (filename) - play the given wav filename (minus .wav)"
  print " probe - probe hosts"
  print " reboot - reboot hosts"
  print " refresh - refresh sound file table on master"
  print " reset - reset hosts"
  print " rescan - rescan sound file table on master"
  print " stop - stop program"
  print " q - exit the program"
  print " upgrade - git upgrade the software and reboot"
  print " vol (val) - set volume to val"
  print

def sendCmd(ip,cmd):
  try:
    request = "http://"+ip+":8080/"+cmd
    if debug: print "sending cmd:",request
    f = urllib.urlopen(request)
    test = f.read()
    print ip,"got response:",test
  except Exception, e:
    print "sndCmd:",repr(e)

def sendToHosts(cmd):
  local = ""
  for h in hosts:
    if adGlobal.isLocalHost(h['ip']):
      local = h['ip']
    else:
      print "sending ",cmd,"command to",h['ip']
      sendCmd(h['ip'],cmd)
  if local != "":
    print "sending ",cmd,"command to local",local
    sendCmd(local,cmd)

def vol(val):
  cmd = "vol?val="+val
  sendToHosts(cmd)

# request;http://192.168.20.104:8080/player?play=filename
def play(filename):
  cmd = "player?play="+filename+".wav"
  sendToHosts(cmd)

def main():
  global hosts
  run=True
  print "getting host list"
  hosts = slp.getHosts("schlub")
  printHostList()
  printCmds()
  while run:
   inp=raw_input("schlub-> ")
   cmd = inp.split(" ");
   if cmd[0] == "q":
     run=False
   elif cmd[0] == "reset":
     hosts = slp.getHosts("schlub")
     printHostList()
   elif cmd[0] == "hosts":
     printHostList()
   elif cmd[0] == "off":
     sendToHosts("poweroff")
   elif cmd[0] == "reboot":
     sendToHosts("reboot")
   elif cmd[0] == "stop":
     sendToHosts("stop")
   elif cmd[0] == "probe":
     sendToHosts("probe")
   elif cmd[0] == "upgrade":
     sendToHosts("upgrade")
   elif cmd[0] == "refresh":
     sendToHosts("refresh")
   elif cmd[0] == "rescan":
     sendToHosts("rescan")
   elif cmd[0] == "auto":
     sendToHosts("auto")
   elif cmd[0] == "manual":
     sendToHosts("manual")

   elif cmd[0] == "vol":
     if len(cmd) == 2:
       vol(cmd[1])
     else:
       print "Error: no volume specified"
   elif cmd[0] == "play":
     if len(cmd) == 2:
       play(cmd[1])
     else:
       print "Error: no filename specified"
   else:
     if len(cmd) == 2 and cmd[1] != "":
       print "Error:",inp
       print
     printCmds()


main()
