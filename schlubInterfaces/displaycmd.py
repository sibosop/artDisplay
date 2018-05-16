#!/usr/bin/env python
import subprocess
import urllib2
import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import adGlobal
import slp
import json

debug=True

hosts = []


def printHostList():
  global hosts
  print "Host list:"
  for h in hosts:
    o = h['ip']
    if 'attr' in h:
      if debug: print "attr",h['attr']
      o += " "+h['attr']
    print " ",o
  print

def sendToHost(ip,cmd):
  print "send to host:",ip,cmd
  url = "http://"+ip+":8080"
  print("url:"+url)
  print("cmd json:"+json.dumps(cmd))
  req = urllib2.Request(url
              ,json.dumps(cmd),{'Content-Type': 'application/json'})
  f = urllib2.urlopen(req)
  test = f.read()
  print("got response:"+test)

def sendToHosts(cmd):
  for h in hosts:
    sendToHost(h['ip'],cmd)

def printCmds():
  print "SchlubCmds:"
  for c in cmds:
    print c
  print

def doCmd(cmd): 
  sendToHosts({'cmd' : cmd[0], 'args' : [""] })
  return 0

def doSound(cmd):
  print "doSound"
  sendToHosts({'cmd' : cmd[0], 'file' : cmd[1]})
  return 0

def doNum(cmd):
  sendToHosts({'cmd' : cmd[0],'args' : [cmd[1]]})
  return 0

def doPhrase(cmd):
  arg = ""
  for c in cmd[1:]:
    arg += c + " "

    
  sendToHosts({'cmd' : cmd[0], 'args' : [arg[:-1]]})
  return 0


def doQuit(cmd):
  print cmd
  return -1

cmds = {
      'Probe'     : doCmd
      ,'Phrase'   : doPhrase
      ,'Poweroff' : doCmd
      ,'Reboot'   : doCmd
      ,'Upgrade'  : doCmd
      ,'Quit' : doQuit
    }


if __name__ == '__main__':
  run=True
  print "getting host list"
  hosts = slp.getHosts("display")
#  hosts = [{'ip' : '192.168.20.112'}]
  printHostList()
  printCmds()
  while run:
    inp=raw_input("schlub-> ")
    cmd = inp.split(" ");
    if cmd[0] in cmds.keys():
      ret = cmds[cmd[0]](cmd)
      if ret == -1:
        run=False
    else:
      print "bad cmd:",inp
      printCmds()


