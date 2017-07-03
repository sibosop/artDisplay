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
numSchlubTracks=3

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
  slp.register("schlub")
  sst = soundServer.soundServerThread(8080)
  sst.setDaemon(True)
  sst.start()
  soundTrack.setup()
  for i in range(numSchlubTracks):
    startEventThread(schlubTrack.schlubTrack())
  im = master.isMaster()
  if im:
    pt = player.playerThread()
    pt.setDaemon(True)
    pt.start()
  while True:
    try:
      time.sleep(5)
    except KeyboardInterrupt:
      syslog.syslog(pname+": keyboard interrupt")
      break
    except Exception as e:
      syslog.syslog(pname+":"+str(e))
      break

  syslog.syslog(pname+" exiting")
  exit(1)

