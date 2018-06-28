#!/usr/bin/env python
import subprocess

import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/schlub")
sys.path.append(home+"/GitProjects/artDisplay/config")
import host
import json
import argparse
import config

debug=True


defParse=None


def printCmds():
  print "SchlubCmds:"
  for c in cmds:
    print c
  print

def sendCargs(p,cargs):
  if len(p.name) + len(p.ip) + len(p.sub) == 0:
    host.sendToHosts(cargs)
    return 0
  if len(p.name) != 0:
    host.sendByName(p.name,cargs)
  if len(p.sub) != 0:
    host.sendWithSubnet(p.sub,cargs)
  if len(p.ip) != 0:
    for h in parms.ip:
      print "h:",h
      host.sendToHost(h,cargs)
  return 0

def doCmd(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parms=parse.parse_args(cmd[1:])
  sendCargs(parms,{'cmd' : cmd[0], 'args' : [""] })
  return 0

def doMasterCmd(cmd):
  host.sendToMaster({'cmd' : cmd[0], 'args' : [""] })
  return 0

def doMasterArg(cmd):
  host.sendToMaster({'cmd' : cmd[0], 'args' : [cmd[1]] })
  return 0
  
def doNum(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('value',type=int,nargs=1)
  parms=parse.parse_args(cmd[1:])
  print parms.value
  sendCargs(parms,{'cmd' : cmd[0], 'args' :  parms.value})
  return 0

def doShow(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('words',nargs='*',default=[])
  parms=parse.parse_args(cmd[1:])
  phrase = ""
  for c in parms.words:
    phrase += c + " "
  args['phrase'] = phrase
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0

langFile = home+"/GitProjects/artDisplay/lists/lang_codes.json"
langs=[]
def getLangs():
  global langs
  if len(langs) == 0:
    with open(langFile) as f:
      langs = json.load(f)
  return langs

def doPhrase(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('words',nargs='*',default=[])
  parse.add_argument('-r','--reps',type=int,nargs=1,default=[1],help='set number of repititions (default 1)')
  parse.add_argument('-v','--vol',type=int,nargs=1,default=[100],help='set volume [default 100]')
  parse.add_argument('-l','--lang',type=str,nargs=1,default=["en"],help='set language',choices=getLangs())
  parse.add_argument('-d','--scat',action='store_true',help='set scatter')
  parms=parse.parse_args(cmd[1:])
  phrase = ""
  for c in parms.words:
    phrase += c + " "
  args = {}
  args['phrase'] = phrase
  args['reps'] = parms.reps[0]
  args['scatter'] = parms.scat
  args['lang'] = parms.lang[0]
  args['vol'] = parms.vol[0]
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0

def doQuit(args):
  print "bye"
  return -1


cmds = {
      'Probe'     : doCmd
      ,'Show'     : doShow
      ,'Volume'   : doNum
      ,'Phrase'   : doPhrase
      ,'Threads'  : doNum
      ,'Poweroff' : doCmd
      ,'Reboot'   : doCmd
      ,'Upgrade'  : doCmd
      ,'PhraseScatter' : doPhrase
      ,'MaxEvents' : doNum
      ,'SoundVol': doNum
      ,'CollectionList' : doMasterCmd
      ,'Collection' : doMasterArg
      ,'Quit' : doQuit
      ,'Help' : printCmds
    }


  


if __name__ == '__main__':
  run=True
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--slp', action='store_true', help='use slp instead of config') 
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  parser.add_argument('-c','--config',nargs=1,type=str,default=[config.defaultSpecPath],help='specify different config file')
  args = parser.parse_args()
  print "config path",args.config
  config.load(args.config[0])
  host.useSlp = args.slp
  host.setHostList()
  host.printHostList()
  printCmds()

    
  cmdParser = argparse.ArgumentParser()
  cmdParser.add_argument('cmd',nargs=1,type=str,default=['Help'],choices=cmds.keys())
  
  while run:
    try:
      inp=raw_input("schlub-> ").split()
      cmdargs = cmdParser.parse_args([inp[0]])
      defParse=argparse.ArgumentParser(add_help=False) 
      defParse.add_argument('-i','--ip',nargs='+',default=[],help='specify dest ip')
      defParse.add_argument('-s','--sub',nargs='+',default=[],help='specify dest ip using subnet')
      defParse.add_argument('-n','--name',nargs='+',default=[],help='specify dest ip by name')
      if cmds[cmdargs.cmd[0]](inp) == -1:
        break
    except KeyboardInterrupt:
      print "bye"
      break
    except Exception, e:
      print "got exception"
      print str(e)
      continue
    except:
      print "parse error"
      continue
        

