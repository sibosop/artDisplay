#!/usr/bin/env python
import os
home = os.environ['HOME']
defaultSpecPath = home+"/GitProjects/artDisplay/config/schlub.json"
import json
specs = None

def load(specPath):
  global specs
  with open(specPath) as f:
    specs = json.load(f)
  
  
