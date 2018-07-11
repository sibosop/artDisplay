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
import argparse

defaultPort = 8085


if __name__ == '__main__':
  pname = sys.argv[0]
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--displayEnable', action = 'store_true',help='set displayEnable')
  args = parser.parse_args()
      
  os.environ['DISPLAY']=":0.0"
  os.chdir(os.path.dirname(sys.argv[0]))
  syslog.syslog(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

  it = recorder.inputThread()
  it.setDaemon(True)

  rt = recog.recogThread(it,args.displayEnable)
  rt.setDaemon(True)

#  analt = anal.analThread(rt)
#  analt.setDaemon(True)
  
  pst = blanket.phraseSender(rt,False) # ALWAYS OFF for now
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

