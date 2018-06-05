#!/usr/bin/env python
import BaseHTTPServer
import threading
import time
import syslog
import os
import sys
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/shared")
sys.path.append(home+"/GitProjects/artDisplay/poem")
import asoundConfig
import upgrade
import soundFile
import master
import json
import displayText

debug=True

def jsonStatus(s):
  d = {}
  d['status'] = s
  return json.dumps(d)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()

  def log_message(self, format, *args):
    syslog.syslog("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

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

class displayServer(BaseHTTPServer.HTTPServer):
  def __init__(self,client,handler):
    BaseHTTPServer.HTTPServer.__init__(self,client,handler)
    self.test = "test var"
    self.cmds = {
      'Probe'     : self.doProbe
      ,'Phrase'   : self.doPhrase
      ,'Poweroff' : self.doPoweroff
      ,'Reboot'   : self.doReboot
      ,'Upgrade'  : self.doUpgrade
    }

  def doPhrase(self,cmd):
    displayText.displayText(cmd['args'][0]);
    return jsonStatus("OK")

  def doPoweroff(self,cmd):
    return jsonStatus("poweroff")

  def doReboot(self,cmd):
    return jsonStatus("reboot")

  def doUpgrade(self,cmd):
    upgrade.upgrade()
    syslog.syslog("returned from upgrade")
    return jsonStatus("reboot")

  def doProbe(self,cmd):
    state = {}
    state['status'] = "ok"
    state['vol'] = 0
    state['isMaster'] = False
    state['sound'] = ""
    state['phrase'] = "phrase"
    return json.dumps(state)


  def handleSchlubCmd(self,cmd):
    if debug: syslog.syslog("handling cmd:"+cmd['cmd']);
    return self.cmds[cmd['cmd']](cmd)

class displayServerThread(threading.Thread):
  def __init__(self,port):
    super(displayServerThread,self).__init__()
    self.port = port
    syslog.syslog("display server:"+str(self.port))
    #self.server_class = BaseHTTPServer.HTTPServer
    self.server_class = displayServer
    self.httpd = self.server_class(('', self.port), MyHandler)

  def run(self):
    self.httpd.serve_forever()

