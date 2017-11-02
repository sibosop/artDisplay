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

def doProbe(h):
  global master
  ip = h['ip']
  print("sending request to ",ip)
  url = "http://"+ip+":8080"
  print("url:",url)
  cmd = { 'cmd' : "Probe" , 'args' : "" }
  req = urllib2.Request(url
            ,json.dumps(cmd),{'Content-Type': 'application/json'})
  f = urllib2.urlopen(req)
  test = f.read()
  print("got response:",test)
  s = json.loads(test)
  print ("is Master",s['isMaster'])
  if ( s['isMaster'] ):
    master = ip

def doRescan():
  global master
  if ( master == "" ):
    print ("NO MASTER NO RESCAN")
    return

  ip = master
  print("sending request to ",ip)
  url = "http://"+ip+":8080"
  print("url:",url)
  cmd = { 'cmd' : "Rescan" , 'args' : "" }
  req = urllib2.Request(url ,json.dumps(cmd),{'Content-Type': 'application/json'})
  f = urllib2.urlopen(req)
  test = f.read()
  print("got response:",test)


print "getting hosts"
hosts = slp.getHosts("schlub")
for h in hosts:
  print h['ip']
  doProbe(h)

print ("master:",master)

first = True
for a in sys.argv:
  try:
    if first:
      first = False
      continue
    for h in hosts:
      cmd = ["scp",a,"pi@"+h['ip']+":/media/pi/SOUND/events/"]
      print cmd
      output = subprocess.check_output(cmd)
  except Exception, e:
    print str(e)

try:
  doRescan()
except Exception, e:
  print str(e)

