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

def sendToHost(ip,cmd,args):
  print "send to host:",ip,cmd,args
  url = "http://"+ip+":8080"
  print("url:"+url)
  cmd = { 'cmd' : cmd , 'args' : args }
  print("cmd json:"+json.dumps(cmd))
  req = urllib2.Request(url
              ,json.dumps(cmd),{'Content-Type': 'application/json'})
  f = urllib2.urlopen(req)
  test = f.read()
  print("got response:"+test)

def sendToHosts(cmd,args):
  for h in hosts:
    sendToHost(h['ip'],cmd,args)

def printCmds():
  print "SchlubCmds:"
  for c in cmds:
    print c
  print

def doCmd(cmd): 
  sendToHosts(cmd[0],[""])
  return 0

def doNum(cmd):
  sendToHosts(cmd[0],[cmd[1]])
  return 0

def doPhrase(cmd):
  arg = ""
  for c in cmd[1:]:
    arg += c + " "

    
  sendToHosts(cmd[0],[arg[:-1]])
  return 0



def doQuit(cmd):
  print cmd
  return -1

cmds = {
      'Probe'     : doCmd
      ,'Volume'   : doNum
      ,'Phrase'   : doPhrase
      ,'Threads'  : doNum
      ,'Poweroff' : doCmd
      ,'Reboot'   : doCmd
      ,'Upgrade'  : doCmd
      ,'PhraseScatter' : doPhrase
      ,'MaxEvents' : doNum
      ,'Quit' : doQuit
    }


if __name__ == '__main__':
  run=True
  print "getting host list"
  hosts = slp.getHosts("schlub")
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


