#!/usr/bin/env python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import time
import syslog
import schlubTrack
import schlub
import os
import sys
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/shared")
import asoundConfig
import upgrade
import soundFile
import master
import player
import json
import schlubSpeak
import blanket
import subprocess
from SocketServer import ThreadingMixIn

debug=True

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
            No further content needed, don't touch this. """

def jsonStatus(s):
  d = {}
  d['status'] = s
  return json.dumps(d)

class MyHandler(BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()

  def log_message(self, format, *args):
    syslog.syslog("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))
  def do_GET(self):
    if debug: syslog.syslog("Get:")
    status =  blanket.getCurrentTranscript()

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(status)
    

  def do_POST(self):
    # Begin the response
    content_len = int(self.headers.getheader('content-length', 0))
    post_body = self.rfile.read(content_len)
    
    if debug: syslog.syslog("Post:"+str(post_body))
    status = self.server.handleSchlubCmd(json.loads(post_body))

    self.send_response(200)
    self.end_headers()
    self.wfile.write(status)
    s = json.loads(status)
    #if debug: syslog.syslog("handle cmd:"+str(s));
    if s['status'] == "poweroff":
      os._exit(3)
    if s['status'] == "reboot":
      os._exit(4)
    if s['status'] == "stop":
      os._exit(5)
    return

class soundServer(HTTPServer):
  def __init__(self,client,handler):
    BaseHTTPServer.HTTPServer.__init__(self,client,handler)
    self.test = "test var"
    self.cmds = {
      'Trans'   : self.doTrans
      ,'Poweroff' : self.doPoweroff
      ,'Reboot'   : self.doReboot
      ,'Upgrade'  : self.doUpgrade
    }
  
  def doTrans(self,cmd):
    return blanket.getCurrentTranscript()

  def doThreads(self,cmd):
    return schlubTrack.changeNumSchlubThreads(int(cmd['args'][0]))

  def doPoweroff(self,cmd):
    return jsonStatus("poweroff")

  def doReboot(self,cmd):
    return jsonStatus("reboot")

  def doUpgrade(self,cmd):
    upgrade.upgrade()
    syslog.syslog("returned from upgrade")
    return jsonStatus("reboot")

  def setPlayMode(self,cmd):
    rval = jsonStatus("not_master")
    if master.isMaster():
      player.enable(cmd['cmd'] == "Auto")
      rval = jsonStatus("ok")
    return rval

  def doRefresh(self,cmd):
    rval = jsonStatus("not_master")
    if master.isMaster():
      soundFile.refresh()
      rval = jsonStatus("ok")
    return rval

  def doRescan(self,cmd):
    rval = jsonStatus("not_master")
    if master.isMaster():
      soundFile.rescan()
      rval = jsonStatus("ok")
    return rval

  def doProbe(self,cmd):
    state = {}
    state['status'] = "ok"
    state['vol'] = asoundConfig.getVolume()
    state['isMaster'] = master.isMaster()
    state['sound'] = schlubTrack.getCurrentSound()
    phrase = schlubSpeak.getCurrentPhrase()
    phrase = phrase.replace("-"," ");
    state['phrase'] = phrase
    state['phraseScatter'] = schlubSpeak.phraseScatter
    state['threads'] = len(schlubTrack.eventThreads)
    state['speaker'] = asoundConfig.getHw()['SpeakerBrand']
    state['auto'] = player.isEnabled() 
    if master.isMaster():
      state['collection'] = soundFile.getCurrentCollection()
      state['maxEvents'] = soundFile.maxEvents
    else:
      state['collection'] = ""
      state['maxEvents'] = 0
    return json.dumps(state)


  def handleSchlubCmd(self,cmd):
    if debug: syslog.syslog("handling cmd:"+cmd['cmd']);
    return self.cmds[cmd['cmd']](cmd)

class transServerThread(threading.Thread):
  def __init__(self,port):
    super(transServerThread,self).__init__()
    host = subprocess.check_output(["hostname","-I"]).split();
    self.host = host[0]
    self.port = port
    syslog.syslog("trans server:"+str(self.host)+":"+str(self.port))
    #self.server_class = BaseHTTPServer.HTTPServer
    #self.server_class = soundServer
    #self.httpd = self.server_class(('', self.port), MyHandler)
    self.server = ThreadedHTTPServer((self.host, self.port), MyHandler)

  def run(self):
    syslog.syslog("starting server")
    self.server.serve_forever()
    syslog.syslog("shouldn't get here");

