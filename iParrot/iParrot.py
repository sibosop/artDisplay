#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
import syslog
import datetime
import time
import recog
import recorder
import anal
import blanket
import transServer

defaultPort = 8085


if __name__ == '__main__':
  pname = sys.argv[0]
  displayEnabled = False
  if len(sys.argv) > 1:
    if sys.argv[1] == '-d':
      displayEnabled = True
      
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  syslog.syslog(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

  it = recorder.inputThread()
  it.setDaemon(True)

  rt = recog.recogThread(it)
  rt.setDaemon(True)

#  analt = anal.analThread(rt)
#  analt.setDaemon(True)
  
  pst = blanket.phraseSender(rt,displayEnabled)
  pst.setDaemon(True)

  it.start()
  rt.start()
#  analt.start()
  pst.start()
  transServer = transServer.transServerThread(defaultPort)
  transServer.setDaemon(True)
  transServer.start()
  while True:
    try:
      time.sleep(2)
    except KeyboardInterrupt:
      syslog.syslog(pname+": keyboard interrupt")
      it.close()
      break
    except Exception as e:
      syslog.syslog(pname+":"+str(e))
      it.close()
      break

  syslog.syslog(pname+" exiting")
  exit(0)

