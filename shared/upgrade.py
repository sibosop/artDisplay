#!/usr/bin/env python
import syslog
import os
import sys
from subprocess import CalledProcessError, check_output
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import adGlobal
debug=True

def upgrade():
  try:
    syslog.syslog("DOING UPGRADE")
    os.chdir(adGlobal.progDir)
    cmd = ['git','pull','--quiet','origin','master']
    output = check_output(cmd)
    if debug: syslog.syslog(output)
  except Exception, e:
    syslog.syslog("player error: "+repr(e))

if __name__ == '__main__':
  upgrade()
  #setVolume(sys.argv[1])
