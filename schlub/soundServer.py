#!/usr/bin/env python
import BaseHTTPServer
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
  def do_GET(s):
    """Respond to a GET request."""
    syslog.syslog("path = "+s.path)
    status = s.server.play(s.path)
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    #s.wfile.write("<html><head><title>Title goes here.</title></head>")
    #s.wfile.write("<body>")
    # If someone went to "http://something.somewhere.net/foo/bar/",
    # then s.path equals "/foo/bar/".
    s.wfile.write(status)
    #s.wfile.write("</body></html>")
    if debug: syslog.syslog("status:"+status)
    s = json.loads(status)
    if s['status'] == "poweroff":
      os._exit(3)
    if s['status'] == "reboot":
      os._exit(4)
    if s['status'] == "stop":
      os._exit(5)

  def log_message(self, format, *args):
    syslog.syslog("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

class soundServer(BaseHTTPServer.HTTPServer):
  def __init__(self,client,handler):
    BaseHTTPServer.HTTPServer.__init__(self,client,handler)
    self.test = "test var"

  def doProbe(self):
    state = {}
    state['status'] = "ok"
    state['vol'] = asoundConfig.getVolume()
    state['isMaster'] = master.isMaster()
    state['sound'] = schlubTrack.getCurrentSound()
    phrase = schlubSpeak.getCurrentPhrase()
    phrase = phrase.replace("-"," ");
    state['phrase'] = phrase
    state['threads'] = len(schlubTrack.eventThreads)
    state['speaker'] = asoundConfig.getHw()['SpeakerBrand']
    state['auto'] = player.isEnabled() 
    return json.dumps(state)

  def play(self,args):
    test=args.split("?")
    rval = jsonStatus("fail")
    if len(test) == 1:
      if test[0] == "/poweroff":
        syslog.syslog("doing power off")
        rval = jsonStatus("poweroff")
      elif test[0] == "/probe":
        syslog.syslog("doing probe")
        rval = self.doProbe();
      elif test[0] == "/stop":
        syslog.syslog("doing stop")
        rval = jsonStatus("stop")
      elif test[0] == "/reboot":
        syslog.syslog("doing reboot")
        rval = jsonStatus("reboot")
      elif test[0] == "/upgrade":
        upgrade.upgrade()
        rval = jsonStatus("reboot")
      elif test[0] == "/auto":
        if master.isMaster():
          player.enable(True)
          rval = jsonStatus("ok")
        else:
          rval = jsonStatus("not_master")
      elif test[0] == "/manual":
        if master.isMaster():
          player.enable(False)
          rval = jsonStatus("ok")
        else:
          rval = jsonStatus("not_master")
      elif test[0] == "/refresh":
        if master.isMaster():
          soundFile.refresh()
          rval = jsonStatus("ok")
        else:
          rval = jsonStatus("not_master")
      elif test[0] == "/rescan":
        if master.isMaster():
          soundFile.rescan()
          rval = jsonStatus("ok")
        else:
          rval = jsonStatus("not_master")
      else:
        syslog.syslog("ignoring:"+args)
        rval = jsonStatus("fail")
    elif len(test) == 2:
      cmds=test[1].split("=")
      if debug: syslog.syslog("test[0]="+test[0])
      if test[0] == "/player":
        if cmds[0] != 'play':
          if debug: syslog.syslog("soundServer ignoring: "+args)
        else:
          if len(cmds) < 2:
            if debug: syslog.syslog("soundServer ignoring: "+args)
          else:
            syslog.syslog("doing "+args)
            rval = schlubTrack.setCurrentSound(cmds[1])
      elif test[0] == "/threads":
        if cmds[0] != 'n':
          if debug: syslog.syslog("soundServer ignoring: "+args)
        else:
          if len(cmds) < 2:
            if debug: syslog.syslog("soundServer ignoring: "+args)
          else:
            syslog.syslog("doing "+args)
            syslog.syslog("cmds[1]"+cmds[1])
            rval = schlubTrack.changeNumSchlubThreads(int(cmds[1]))
      elif test[0] == "/phrase":
        if cmds[0] != 'p':
          if debug: syslog.syslog("soundServer ignoring: "+args)
        else:
          if len(cmds) < 2:
            if debug: syslog.syslog("soundServer ignoring: "+args)
          else:
            syslog.syslog("doing "+args)
            syslog.syslog("cmds[1]"+cmds[1])
            rval = schlubSpeak.setCurrentPhrase(cmds[1])
      elif test[0] == "/vol":
        if cmds[0] != 'val':
          if debug: syslog.syslog("soundServer ignoring: "+args)
        else:
          if len(cmds) < 2:
            if debug: syslog.syslog("soundServer ignoring: "+args)
          else:
            syslog.syslog("doing "+args)
            syslog.syslog("cmds[1]"+cmds[1])
            asoundConfig.setVolume(cmds[1])
          rval = jsonStatus("ok")
      else:
        if debug: syslog.syslog("soundServer ignoring:"+args)
          
    return rval;


class soundServerThread(threading.Thread):
  def __init__(self,port):
    super(soundServerThread,self).__init__()
    self.port = port
    syslog.syslog("sound server:"+str(self.port))
    #self.server_class = BaseHTTPServer.HTTPServer
    self.server_class = soundServer
    self.httpd = self.server_class(('', self.port), MyHandler)

  def run(self):
    self.httpd.serve_forever()

