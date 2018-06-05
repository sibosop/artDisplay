#!/usr/bin/env python
import glob 
import subprocess

poets = ['Shakespeare','emily','browning']
poemDir = '/media/pi/POEMDATA'

for p in poets:
  candidates = glob.glob(poemDir+"/"+p+"/*/*.txt")
  for l in candidates:
    print l
    n = l.find(p)
    print l[n:]
    subprocess.check_output(["cp",l,l[n:]])


