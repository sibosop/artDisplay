#!/usr/bin/env python
import subprocess
import urllib
import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import adGlobal

debug=False

hosts = []
def setHostList():
  print "getting host addresses..."
  global hosts
  hosts=[]
  services = subprocess.check_output(["slptool"
                  ,"findsrvs","service:schlub.x"]).split('\n')
  if len(services) == 0:
    if debug: print "no available services"
  for s in services:
    if debug: print "slp s:",s
    loc=s.split(',');
    if loc[0] == '':
      continue
    if debug: print("loc:",str(loc))
    attr=subprocess.check_output(["slptool","findattrs",loc[0]]);
    attr=attr.strip()
    if debug: print "attr:",attr
    host={}
    host['attr']=attr
    host['ip']=loc[0].split("//")[1]
    if debug: print("slp host",str(host))
    hosts.append(host)


def printHostList():
  print "Host list:"
  for h in hosts:
    o = h['ip']
    if h['attr']:
      if debug: print "attr",h['attr']
      o += " "+h['attr']
    print " ",o
  print

def printCmds():
  print "SchlubCmds:"
  print " q - exit the program"
  print " hosts - print host list"
  print " reset - reset hosts"
  print " off - power off hosts"
  print " reboot - reboot hosts"
  print " pause - pause hosts"
  print " stop - stop program"
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

def main():
  run=True
  setHostList()
  printHostList()
  printCmds()
  while run:
   inp=raw_input("schlub-> ")
   cmd = inp.split(" ");
   if cmd[0] == "q":
     run=False
   elif cmd[0] == "reset":
     setHostList()
     printHostList()
   elif cmd[0] == "hosts":
     printHostList()
   elif cmd[0] == "off":
     sendToHosts("poweroff")
   elif cmd[0] == "reboot":
     sendToHosts("reboot")
   elif cmd[0] == "stop":
     sendToHosts("stop")
   elif cmd[0] == "pause":
     pause()
   elif cmd[0] == "vol":
     if len(cmd) == 2:
       vol(cmd[1])
     else:
       print "Error: no volume specified"
   else:
     if len(cmd) == 2 and cmd[1] != "":
       print "Error:",inp
       print
     printCmds()


main()
