#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
import syslog
import slp
import soundServer
import player
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import master
import syslog
import datetime
import time
import schlubTrack
import soundTrack

debug = False
numSchlubThreads=3
schlubExit = 0

eventThreads=[]
def startEventThread(t):
  global eventThreads
  eventThreads.append(t)
  eventThreads[-1].setDaemon(True)
  eventThreads[-1].start()

if __name__ == '__main__':
  pname = sys.argv[0]
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  syslog.syslog(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  
  slp.start()
  im = master.isMaster()
  attr=""
  if im:
    attr="master=true"
  slp.register("schlub",attr)
  sst = soundServer.soundServerThread(8080)
  sst.setDaemon(True)
  sst.start()
  soundTrack.setup()
  schlubTrack.changeNumSchlubThreads(numSchlubThreads)
  if im:
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

