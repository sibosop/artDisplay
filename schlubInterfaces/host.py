#!/usr/bin/env python
import sys
import os
home = os.environ['HOME']
import sys
import json
import urllib2

hosts = []
def getHostList():
  global hosts
  if len(sys.argv) > 1:
    print "getting lost list from arguments"
    first = True
    for a in sys.argv:
      if first:
        first = False
        continue
      e = {}
      e['ip'] = a
      #print "adding:",e
      hosts.append(e)
  else:
    import slp
    print "getting host list from slp"
    hosts = slp.getHosts("schlub")

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
    f = urllib2.urlopen(req)
    test = f.read()
    print("got response:"+test)
  except Exception as e:
    print "host send error:",str(e)

def sendToHosts(cmd):
  for h in hosts:
    sendToHost(h['ip'],cmd)

if __name__ == '__main__':
  run=True
  getHostList()
  printHostList()
