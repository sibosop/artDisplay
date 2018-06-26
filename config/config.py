#!/usr/bin/env python
import os
home = os.environ['HOME']
specPath = home+"/GitProjects/artDisplay/config/schlub.json"
import json
specs = None

with open(specPath) as f:
  specs = json.load(f)
  
  
