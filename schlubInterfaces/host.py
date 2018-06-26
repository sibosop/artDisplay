#!/usr/bin/env python
import sys
import os
import argparse
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/config")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import sys
import json
import urllib2
import config

useSlp = False
hosts = []
def getHostList():
  global hosts
  if useSlp:
    import slp
    #print "getting host list from slp"
    hosts = slp.getHosts("schlub")
  else:
    #print "getting host from specs"
    if len(hosts) != 0:
      return
    for a in config.specs['hosts']:
      hosts.append(a)


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

def sendToHost(ip,cmd):
  try:
    print "send to host:",ip,cmd
    url = "http://"+ip+":8080"
    print("url:"+url)
    print("cmd json:"+json.dumps(cmd))
    req = urllib2.Request(url
                ,json.dumps(cmd),{'Content-Type': 'application/json'})
    timeout = 4
    f = urllib2.urlopen(req,None,timeout)
    test = f.read()
    print("got response:"+test)
  except Exception as e:
    print "host send error:",str(e)

def sendToHosts(cmd):
  for h in hosts:
    sendToHost(h['ip'],cmd)

if __name__ == '__main__':
  run=True
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config', action='store_true', help='clear the display on exit') 
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  args = parser.parse_args()
  specs = None
  if args.config:
    specs = config.load()
  getHostList(specs)
  printHostList()
