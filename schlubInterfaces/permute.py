#!/usr/bin/env python 
import os
home = os.environ['HOME']
import sys
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import slp
import subprocess
import urllib2
import json
import glob


if len(sys.argv) !=3:
  print "usage:",sys.argv[0]," srcDir"," ext"
path = sys.argv[1]+'/*__'+sys.argv[2]+".wav";
fs = glob.glob(path)
print "name,enabled,maxVol"
post = ",1,0.7"
for f in fs:
  f = os.path.basename(f)
  for f1 in fs:
    f1 = os.path.basename(f1)
    if f == f1:
      print f+post
    else:
      print f+"&"+f1+post


