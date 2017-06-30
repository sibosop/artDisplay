#!/usr/bin/env python

import threading
import time
import syslog
import subprocess

debug = True
class playerThread(threading.Thread):
  def run(self):
    while True:
      time.sleep(10)
      hosts = []
      try:
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
      except KeyboardInterrupt:
        return
