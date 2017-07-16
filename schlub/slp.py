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

def getHosts(name):
  _hosts = []
  services = subprocess.check_output(["slptool"
                        ,"findsrvs","service:"+name+".x"]).split('\n')
  if len(services) == 0:
    syslog.syslog("no available services")
    return _hosts
  for s in services:
    if debug: syslog.syslog("slp s:"+s)
    loc=s.split(',');
    if loc[0] == '':
      continue
    if debug: syslog.syslog("loc:"+str(loc))
    #attr=subprocess.check_output(["slptool","findattrs",loc[0]]);
    host={}
    host['ip']=loc[0].split("//")[1]
    if debug: syslog.syslog("slp host"+str(host))
    _hosts.append(host)
  return _hosts

if __name__ == '__main__':
  hosts = getHosts("schlub")
  for h in hosts:
    print h['ip']
