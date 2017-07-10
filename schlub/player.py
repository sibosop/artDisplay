#!/usr/bin/env python

import threading
import time
import syslog
import subprocess
import glob
import adGlobal
import sys
import random
import urllib
import soundFile


debug = True
class playerThread(threading.Thread):
  def run(self):
    edir = adGlobal.eventDir
    while True:
      try:
        time.sleep(random.randint(5,10))
        hosts = []
        services = subprocess.check_output(["slptool"
                        ,"findsrvs","service:schlub.x"]).split('\n')
        if len(services) == 0:
          syslog.syslog("no available services")
          continue
        for s in services:
          if debug: syslog.syslog("slp s:"+s)
          loc=s.split(',');
          if loc[0] == '':
            continue
          if debug: syslog.syslog("loc:"+str(loc))
          attr=subprocess.check_output(["slptool","findattrs",loc[0]]);
          host={}
          host['ip']=loc[0].split("//")[1]
          if debug: syslog.syslog("slp host"+str(host))
          hosts.append(host)
        e = soundFile.getSoundEntry()
        choice = e.name
        if debug: syslog.syslog("player choosing "+choice)
        for h in hosts:
          ip = h['ip']
          if debug: syslog.syslog("sending request to "+ip)
          request = "http://"+ip+":8080/player?play="+choice
          if debug: syslog.syslog("request;"+request)
          f = urllib.urlopen(request)
          test = f.read()
          if debug: syslog.syslog("got response:"+test)
      except Exception, e:
        syslog.syslog("player error: "+repr(e))
