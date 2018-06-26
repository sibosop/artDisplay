#!/usr/bin/env python
import os
home = os.environ['HOME']
specPath = home+"/GitProjects/artDisplay/config/schlub.json"
import json

specs = None
def load():
  with open(specPath) as f:
    specs = json.load(f)
  return specs
  
  