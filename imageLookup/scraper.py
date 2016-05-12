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


debug=False
def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)), "html5lib")
  #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url)), "html.parser")
  
def scraper(choices,image_type):
  images=[]
  query=html_escape(choices[0])+'+'+html_escape(choices[1])
  url="http://www.google.com/images?q="+query
  if debug: print "url:",url
  header = {'User-Agent': 'Mozilla/5.0'} 
  soup = get_soup(url,header)
  images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
  if debug: print "num images:",len(images)
  return images

if __name__ == '__main__':
  images=[]
  w=words.Words()
  choices=[]
  while len(images) < 20:
    choices=w.getWords()
    images=scraper(choices,"Action")
  for t in choices:
    print t
  for i in images:
    print i
