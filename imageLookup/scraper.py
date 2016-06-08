#!/usr/bin/env python
import os

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import time
import adGlobal
import syslog
import subprocess
import glob
import words
import httplib, urllib, base64
import json
import sys
import google
from py_bing_search import PyBingImageSearch
debug=False


headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '883e1d2b72b743f8aad86451b97c91df',
}


html_escape_table = {
  "&": "&amp;",
  '"': "&quot;",
  "'": "%27",
  ">": "&gt;",
  "<": "&lt;",
  " ": "+"
}
def html_escape(text):
  """Produce entities within text."""
  if debug: print "text:",text
  return "".join(html_escape_table.get(c,c) for c in text)



def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)), "html5lib")
  #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url)), "html.parser")
  
#@profile
def scraper(choices):
  images=[]
  if adGlobal.searchType == "Google-old":
    if debug: print "doing Google fetch"
    query=html_escape(choices[0])+'+'+html_escape(choices[1])
    url="http://www.google.com/images?q="+query
    if debug: print "url:",url
    header = {'User-Agent': 'Mozilla/5.0'} 
    soup = get_soup(url,header)
    images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
  elif adGlobal.searchType == "Google":
    if debug: print "doing Google CSE"
    return google.getImages(choices)
  elif adGlobal.searchType == "Bing":
    if debug: print "doing bing fetch"
    choices[0]=choices[0].replace(" ","+")
    choices[1]=choices[1].replace(" ","+")
    try:
        params = urllib.urlencode({
            # Request parameters
            'q': choices[0]+' '+choices[1],
            'count': '50',
            'offset': '0',
            'mkt': 'en-us',
            'safeSearch': 'off',
        })
        if debug: print "params:", params
        conn = httplib.HTTPSConnection('bingapis.azure-api.net')
        conn.request("GET", "/api/v5/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        if debug: print "data type",type(data)
        if debug:
          for key in data.keys():
            print "k:",key,"v:",data[key]
        results=data['value']
        if debug: print "num vals",len(results)
        for i in results:
          if debug: print "i['contentUrl']:",i['contentUrl']
          relem={}
          relem['full']=i['contentUrl']
          relem['thumb']=i['thumbnailUrl']
          images.append(relem)
        conn.close()
    except:
      e = sys.exc_info()[0]
      print "return from exception "+str(e)
      time.sleep(10)
  else:
    if debug: print "doing archive fetch"
  if debug: print "num images:",len(images)
  return images

if __name__ == '__main__':
  images=[]
  choices=[]
  while len(images) < 20:
    choices=words.getWords()
    images=scraper(choices[:])
  for t in choices:
    print t
  for i in images:
    print i
