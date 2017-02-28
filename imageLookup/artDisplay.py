#!/usr/bin/env python
import sys
import os
import syslog
import subprocess
import threading
import textChecker
import master
import imageLookup
import imageChecker
import panel
import time
import datetime
import traceback
import signal
import schedule
import adGlobal
import dispTextChecker

def watchdog(signum,frame):
  syslog.syslog("watchdog handler rebooting")
  syslog.syslog(traceback.format_exc())
  #subprocess.check_output(["sudo","reboot"])
  time.sleep(10)
  exit(-1)

def changeSearch(s):
  syslog.syslog("changing search type to "+s)
  adGlobal.searchType = s
  

if __name__ == '__main__':
  syslog.syslog("art display at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  debug = True
  signal.signal(signal.SIGALRM, watchdog)
  os.chdir(os.path.dirname(sys.argv[0]))
  syslog.syslog("starting artDisplay.py")
  host = subprocess.check_output(["hostname","-I"]).split();
  if debug:
    syslog.syslog("host ="+host[0])
    
  test = subprocess.check_call(["sudo","service","slpd","start"])
  regs=["slptool","register","service:artdisplay.x://"+host[0]]
  hp=panel.hasPanel()
  if hp:
    regs.append("hasPanel=true")

  dt = master.isDispText();
  if dt:
    regs.append("isDispText=true");

  if debug: syslog.syslog("regs:"+str(regs));
  test = subprocess.check_call(regs)

  try:
    os.environ["DISPLAY"] = ":0.0"
    tc = threading.Thread(target=textChecker.textChecker)
    tc.setDaemon(True)
    
    if hp:
      tc.start()

    td = threading.Thread(target=dispTextChecker.dispTextChecker)
    td.setDaemon(True);
    if dt:
      syslog.syslog("starting text disp daemon");
      td.start()
    
    im = master.isMaster()
    ti = threading.Thread(target=imageLookup.imageLookup)
    ti.setDaemon(True)
    if im:
      ti.start()  

    tic = threading.Thread(target=imageChecker.imageChecker)
    tic.setDaemon(True)
    if dt is False:
      tic.start()
    #schedule.every().day.at("07:34").do(changeSearch,"Google")
    #schedule.every().day.at("08:14").do(changeSearch,"Archive")
    #schedule.every().day.at("20:00").do(changeSearch,"Bing")
    #schedule.every().day.at("20:30").do(changeSearch,"Archive")
    while True:
      schedule.run_pending()
      if hp:
        tc.join(1)  
      if im:
        ti.join(1)
      if dt:
        td.join(1)
      else:
        tic.join(1)
  except:
    e = sys.exc_info()[0]
    syslog.syslog("return from exception "+str(e))
