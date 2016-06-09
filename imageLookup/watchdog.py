#!/usr/bin/env python
import signal
import threading
import time
import traceback
import subprocess
import syslog


def watchdog(signum,frame):
  syslog.syslog("watchdog handler rebooting")
  subprocess.check_output(["sudo","reboot"])
  time.sleep(10)
  
def testThread():
  len  = 1
  while True:
    signal.alarm(5)
    print "testThread len",len
    time.sleep(len)
    len += 1

if __name__ == '__main__':
  tc = threading.Thread(target=testThread)
  signal.signal(signal.SIGALRM, watchdog)
  tc.setDaemon(True)
  tc.start()

  while tc.is_alive(): tc.join(1)
