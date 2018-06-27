#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
import syslog
import soundServer
import player
sys.path.append(home+"/GitProjects/artDisplay/schlubInterfaces")
sys.path.append(home+"/GitProjects/artDisplay/config")
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import adGlobal
import slp
import master
import syslog
import datetime
import time
import schlubTrack
import soundTrack
import schlubSpeak
import config
import argparse
import host

debug = False
numSchlubThreads=1
schlubExit = 0

eventThreads=[]
def startEventThread(t):
  global eventThreads
  eventThreads.append(t)
  eventThreads[-1].setDaemon(True)
  eventThreads[-1].start()

if __name__ == '__main__':
  adGlobal.hasAudio = True
  pname = sys.argv[0]
  syslog.syslog(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--slp', action='store_true', help='use slp instead of config') 
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  parser.add_argument('-c','--config',nargs=1,type=str,default=[config.defaultSpecPath],help='specify different config file')
  if debug: syslog.syslog("config path"+args.config[0])
  args = parser.parse_args()
  config.load(args.config[0])
  im = master.isMaster()
  host.useSlp = args.slp
  if args.slp:
    attr=""
    if im:
      attr="master=true"
    slp.start()
    slp.register("schlub",attr)

  sst = soundServer.soundServerThread(8080)
  sst.setDaemon(True)
  sst.start()
  soundTrack.setup()
  schlubTrack.changeNumSchlubThreads(numSchlubThreads)
  speakThread = schlubSpeak.schlubSpeakThread()
  speakThread.setDaemon(True)
  speakThread.start()
  if im:
    syslog.syslog("starting player")
    pt = player.playerThread()
    pt.setDaemon(True)
    pt.start()
  while schlubExit == 0:
    try:
      time.sleep(5)
    except KeyboardInterrupt:
      syslog.syslog(pname+": keyboard interrupt")
      break
    except Exception as e:
      syslog.syslog(pname+":"+str(e))
      break

  syslog.syslog(pname+" exiting")
  exit(schlubExit)

