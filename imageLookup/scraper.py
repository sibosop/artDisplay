#!/usr/bin/env python
import os
import random
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import time
import adGlobal
import syslog
import subprocess
import glob


html_escape_table = {
  "&": "&amp;",
  '"': "&quot;",
  "'": "%27",
  ">": "&gt;",
  "<": "&lt;",
  }

def html_escape(text):
  """Produce entities within text."""
  if debug: print "text:",text
  return "".join(html_escape_table.get(c,c) for c in text)


debug=True
def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)), "html5lib")
  #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url)), "html.parser")
  
def scraper(lines,image_type):
  images=[]
  while len(images) < 20:
    images=[]
    tests=[]
    for i in range(0,2):
      n = random.randint(0,len(lines)-1)
      tests.append(html_escape(lines[n]))
    if debug: print "tests:",tests[0],tests[1] #,tests[2]
  
    query=tests[0]+'+'+tests[1]
    url="http://www.google.com/images?q="+query
    if debug: print "url:",url
    header = {'User-Agent': 'Mozilla/5.0'} 
    soup = get_soup(url,header)
    images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
    if debug: print "num images:",len(images)

  return [images,tests]

if __name__ == '__main__':
  wordFile = adGlobal.wordFile
  lines = open(wordFile).read().split('\n')
  ret=scraper(lines,"Action")
  for t in ret[1]:
    print t
  for i in ret[0]:
    print i
