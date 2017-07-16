#!/usr/bin/env python 
import sys
import slp
import subprocess

print "getting hosts"
hosts = slp.getHosts("schlub")
for h in hosts:
  print h['ip']

first = True
for a in sys.argv:
  try:
    if first:
      first = False
      continue
    for h in hosts:
      cmd = ["scp",a,"pi@"+h['ip']+":/media/pi/SOUND/events/"]
      print cmd
      output = subprocess.check_output(cmd)

  except Exception, e:
    print str(e)


