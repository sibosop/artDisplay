#!/usr/bin/env python
import subprocess
import syslog


debug=True

def start():
  test = subprocess.check_call(["sudo","service","slpd","start"])


def register(service,attr=""):
  host = subprocess.check_output(["hostname","-I"]).split();
  shost = host[0]
  subnet = "1"
  for h in host:
    if debug: syslog.syslog("check host ="+h)
    v = h.split('.')
    if debug: syslog.syslog("test host:"+str(v))
    if len(v) == 4 and v[2] == subnet:
      shost = h
      if debug: syslog.syslog("found subnet " 
        + subnet 
        + " using:" + shost)
      break
  syslog.syslog("shost ="+shost)
  regs=["slptool","register","service:"+service+".x://"+shost]
  if debug: syslog.syslog("attr:"+attr)
  if attr != "":
    regs.append(attr)
  if debug: syslog.syslog("regs:"+str(regs))
  test = subprocess.check_call(regs)
