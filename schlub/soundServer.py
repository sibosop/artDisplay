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

class soundServer(BaseHTTPServer.HTTPServer):
  def __init__(self,client,handler):
    BaseHTTPServer.HTTPServer.__init__(self,client,handler)
    self.test = "test var"
    self.cmds = {
      'Probe'     : self.doProbe
      ,'Sound'    : self.doSound
      ,'Volume'   : self.doVolume
      ,'Phrase'   : self.doPhrase
      ,'Threads'  : self.doThreads
      ,'Poweroff' : self.doPoweroff
      ,'Reboot'   : self.doReboot
      ,'Upgrade'  : self.doUpgrade
      ,'Auto'     : self.setPlayMode
      ,'Manual'   : self.setPlayMode
      ,'Refresh'  : self.doRefresh
      ,'Rescan'   : self.doRescan
      ,'SoundList': self.doSoundList
      ,'SoundEnable' : self.doSoundEnable
      ,'CollectionList': self.doCollectionList
      ,'Collection' : self.doCollection
      ,'PhraseScatter' : self.doPhraseScatter
    }

  def doPhraseScatter(self,cmd):
    return schlubSpeak.setPhraseScatter(cmd['args'][0])

  def doSoundEnable(self,cmd):
    return soundFile.setSoundEnable(cmd['args'][0],cmd['args'][1])
  def doSoundList(self,cmd):
    return soundFile.getSoundList();
  def doSound(self,cmd):
    return schlubTrack.setCurrentSound(cmd['args'][0])

  def doCollectionList(self,cmd):
    return soundFile.getCollectionList()
  def doCollection(self,cmd):
    syslog.syslog(str(cmd))
    return soundFile.setCurrentCollection(cmd['args'][0])


  def doVolume(self,cmd):
    asoundConfig.setVolume(cmd['args'][0])
    return jsonStatus("ok")

  def doPhrase(self,cmd):
    return schlubSpeak.setCurrentPhrase(cmd['args'][0])

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
    else:
      state['collection'] = ""
    return json.dumps(state)


  def handleSchlubCmd(self,cmd):
    if debug: syslog.syslog("handling cmd:"+cmd['cmd']);
    return self.cmds[cmd['cmd']](cmd)

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

