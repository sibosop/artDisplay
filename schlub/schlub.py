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

debug = False
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

