#!/usr/bin/env python

import threading
import time
import sys
import syslog
import subprocess
import glob
import os
import urllib2
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/shared")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import slp
import words
import random
import json

debug = True
class phraseLookupThread(threading.Thread):
  def run(self):
    while True:
      try:
        hosts = slp.getHosts("schlub")
        list = words.getWords()
        phrase = ""
        for w in list:
          phrase += w + " "
        if debug: syslog.syslog("phrase lookup:"+phrase)
        seq = []
        for h in hosts:
          seq.append(h['ip'])
        ip = random.choice(seq)
        if debug: syslog.syslog("sending request to "+ip)
        url = "http://"+ip+":8080"
        if debug: syslog.syslog("url:"+url)
        cmd = { 'cmd' : "Phrase" , 'args' : [phrase] }
        if debug: syslog.syslog("cmd json:"+json.dumps(cmd))
        req = urllib2.Request(url
                    ,json.dumps(cmd),{'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        test = f.read()
        if debug: syslog.syslog("got response:"+test)
        stime = random.randint(15,40)
        time.sleep(stime)
      except Exception, e:
        syslog.syslog("phrasePlayerError:"+repr(e));

