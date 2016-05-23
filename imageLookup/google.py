#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.

Command-line application that does a search.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import pprint
import adGlobal
from apiclient.discovery import build

global initFlag
initFlag=False
debug=False
global creds
creds={}

def doSetup():
  global creds
  lines = open(adGlobal.credFile).read().split('\n')
  for l in lines:
    vars=l.split("=")
    if len(vars) == 2:
      creds[vars[0]]=vars[1]

  for k in creds.keys():
    if debug: print "key:",k,"value:",creds[k]
  

  
def getImages(qs):
  global initFlag
  if initFlag==False:
    doSetup()
    initFlag=True
  images=[]
  index=0
  while len(images) < 15:
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build("customsearch", "v1",
              developerKey=creds['key'])
    query = qs[0]+" "+qs[1]
    startReq = index * 10
    
    if debug: print "query:",query,"index:",startReq
    res=None
    if index == 0:
      res = service.cse().list(
          q=query,
          cx=creds['cx'],
          searchType='image',
          safe='medium',
        ).execute()
    else:
      res = service.cse().list(
          q=query,
          cx=creds['cx'],
          searchType='image',
          start=int(startReq),
          safe='medium',
        ).execute()
    if debug: print "type:",type(res),"num items:",len(res['items'])
    if len(res['items']) < 10:
      if debug: print "rejecting to few items"
      return []

    #if debug: print "res:",res 
    for l in res['items']:
      if debug: print "link",l['link']
      images.append(l['link'])
  
    index += 1
        
    #if debug: pprint.pprint(res)

  return images


if __name__ == '__main__':
  import words
  images=getImages(words.getWords())
  for i in images:
    print i
