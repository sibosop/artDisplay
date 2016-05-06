#!/usr/bin/env python
import platform
home="/home/pi"

plats=platform.platform().split('-');
if plats[0] == 'Darwin':
  home="/Users/brian"


cacheDir=home+"/ImageCache"
wordFile=home+"/GitProjects/artDisplay/imageLookup/corncob_lowercase.txt"