#!/usr/bin/env python 
import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import slp
import subprocess
import urllib2
import json
master=""

def sendCmd(ip,cmd):
  print("sending request to ",ip)
  url = "http://"+ip+":8080"
  print("url:",url)
  req = urllib2.Request(url
            ,json.dumps(cmd),{'Content-Type': 'application/json'})
  f = urllib2.urlopen(req)
  test = f.read()
  print("got response:",test)
  s = json.loads(test)
  return s
  
def doProbe(h):
  global master
  ip = h['ip']
  cmd = { 'cmd' : "Probe" , 'args' : "" }
  s = sendCmd(ip,cmd)
  print ("is Master",s['isMaster'])
  if ( s['isMaster'] ):
    master = ip


print "getting hosts"
hosts = slp.getHosts("schlub")
for h in hosts:
  print h['ip']
  doProbe(h)

print ("master:",master)
cmd = { 'cmd' : "CollectionList" , 'args' : "" }
s = sendCmd(master,cmd)
count = 1
for c in s['collections']:
  print (str(count)+": "+c)
  count += 1
  
try:
  choice = int(raw_input("Enter collection num:"))
  if choice > 0 and choice <= count:
    cmd = { 'cmd' : "Collection", 'args' : [s['collections'][choice-1]] }
    print cmd
    s = sendCmd(master,cmd)
    print s
except ValueError:
  print "bad choice"
print "done"
