#!/usr/bin/env python
import subprocess

import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import host
import json

debug=True




def printCmds():
  print "SchlubCmds:"
  for c in cmds:
    print c
  print

def doCmd(cmd): 
  host.sendToHosts({'cmd' : cmd[0], 'args' : [""] })
  return 0

def doSound(cmd):
  print "doSound"
  host.sendToHosts({'cmd' : cmd[0], 'file' : cmd[1]})
  return 0

def doNum(cmd):
  host.sendToHosts({'cmd' : cmd[0],'args' : [cmd[1]]})
  return 0

def doShow(cmd):
  phrase = ""
  for c in cmd[1:]:
    phrase += c + " "
  phrase = phrase[:-1]
  args = {}
  args['phrase'] = phrase
  args['reps'] = 2
  args['scatter'] = False

  host.sendToHosts({'cmd' : cmd[0], 'args' : args})
  return 0

def doPhrase(cmd):
  phrase = ""
  reps = int(cmd[1:][0])
  vol = int(cmd[2:][0])
  for c in cmd[3:]:
    phrase += c + " "
  phrase = phrase[:-1]
  args = {}
  args['phrase'] = phrase
  args['reps'] = reps
  args['scatter'] = False
  args['lang'] = 'en-uk'
  args['vol'] = vol

  host.sendToHosts({'cmd' : cmd[0], 'args' : args})
  return 0

langFile = home+"/GitProjects/artDisplay/lists/lang_codes.json"
def doSetLang(cmd):
  with open(langFile, 'r') as myfile:
    data = myfile.read()
  print data


def doQuit(cmd):
  print cmd
  return -1


cmds = {
      'Probe'     : doCmd
      ,'Sound'    : doSound
      ,'Show'     : doShow
      ,'Volume'   : doNum
      ,'Phrase'   : doPhrase
      ,'Threads'  : doNum
      ,'Poweroff' : doCmd
      ,'Reboot'   : doCmd
      ,'Upgrade'  : doCmd
      ,'PhraseScatter' : doPhrase
      ,'MaxEvents' : doNum
      ,'SetLang' : doSetLang
      ,'SoundVol': doNum
      ,'Quit' : doQuit
    }


  


if __name__ == '__main__':
  run=True
  host.getHostList()
  host.printHostList()
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


