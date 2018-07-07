#!/usr/bin/env python
import sys
import os
import argparse
import platform
import subprocess
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/config")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import sys
import json
import urllib2
import config

useSlp = False
hosts = []
names = []
timeout = 2
def setHostList():
  global hosts
  if useSlp:
    import slp
    #print "getting host list from slp"
    hosts = slp.getHosts("schlub")
  else:
    if debug: print "getting host from specs"
    if config.specs == None:
      config.load()
    if len(hosts) == 0:
      for a in config.specs['hosts']:
        hosts.append(a)
        if 'name' in a:
          names.append(a['name'])
  return hosts

def getHosts():
  global hosts
  if len(hosts) == 0:
    setHostList()
  return hosts
  
def getHostIps():
  rval = []
  for h in hosts:
    rval.append(h['ip'])
  return rval

def printHostList():
  global hosts
  print "Host list:"
  for h in hosts:
    #print "h:",h
    o = h['ip']
    if 'attr' in h:
      if debug: print "attr",h['attr']
      o += " "+h['attr']
    print " ",o
  print

def sendToMaster(cmd):
  for h in hosts:
    if h['isMaster']:
      sendToHost(h['ip'],cmd)
      break

def sendByName(nameList,cmd):
  for n in nameList:
    for h in config.specs['hosts']:
      if h['name'] == n:
        sendToHost(h['ip'],cmd)
        break
        
def sendToHost(ip,cmd):
  rval = True
  try:
    if debug: print "send to host:",ip,cmd
    url = "http://"+ip+":8080"
    if debug: print("url:"+url)
    if debug: print("cmd json:"+json.dumps(cmd))
    req = urllib2.Request(url
                ,json.dumps(cmd),{'Content-Type': 'application/json'})
    f = urllib2.urlopen(req,None,timeout)
    test = f.read()
    if debug: print("got response:"+test)
  except Exception as e:
    if debug: print "host send error:",str(e)
    rval = False
  return rval

def sendWithSubnet(ip,cmd):
  for i in ip:
    h = config.specs['subnet']+"."+i
    sendToHost(h,cmd)

def sendToHosts(cmd):
  for h in hosts:
    sendToHost(h['ip'],cmd)

debug = False
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


if __name__ == '__main__':
  run=True
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--slp', action='store_true', help='clear the display on exit') 
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  args = parser.parse_args()
  useSlp = args.slp
  getHostList()
  printHostList()
  for h in hosts:
    if isLocalHost(h['ip']):
      print h['ip'],"is local host"
