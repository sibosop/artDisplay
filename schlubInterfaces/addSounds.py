#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import slp
import master
import syslog
import datetime
import time
import adGlobal
import threading
import phraseLookup
import json
import urllib2
import subprocess

debug = True

if __name__ == '__main__':
  pname = sys.argv[0]
  os.chdir(os.path.dirname(sys.argv[0]))
  print(pname," at ",datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  master = ""
  try:
    print "retrieving hosts..."
    hosts = slp.getHosts("schlub")
    for host in hosts:
      cmd = { 'cmd' : "Probe" , 'args' : "" }
      url = "http://"+host['ip']+":8080"
      req = urllib2.Request(url ,json.dumps(cmd),{'Content-Type': 'application/json'})
      f = urllib2.urlopen(req)
      test = f.read()
      if debug: print("got response:",test)
      response = json.loads(test)
      if response['isMaster'] == True:
        print host['ip'],"is master"
        master = host['ip'] 
        break;
    if master == "":
      print "no master!"
      exit(-1)
    for file in sys.argv[1:]:
      print file
      for host in hosts:
        cmd = ['scp',file,"pi@"+host['ip']+":"+adGlobal.eventDir]
        print cmd
        subprocess.check_output(cmd)
    cmd = { 'cmd' : "Rescan" , 'args' : "" }
    url = "http://"+master+":8080"
    print "url:",url,"cmd:",json.dumps(cmd)
    req = urllib2.Request(url ,json.dumps(cmd),{'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    test = f.read()
    if debug: print("got response:",test)
  except Exception, e:
    print("phrasePlayerError:",repr(e));
    
