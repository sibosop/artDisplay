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

debug=True

def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)), "html5lib")
  #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url)), "html.parser")

def imageLookup():
  DIR = adGlobal.getCacheDir();
  
  wordFile = adGlobal.wordFile;
  maxImagesPerHost = 3
  lines = open(wordFile).read().split('\n')
  while True:
    hosts=[]
    services = subprocess.check_output(["slptool","findsrvs","service:artdisplay.x"]).split('\n');
    if len(services) == 0:
      syslog.syslog("no available services")
      time.sleep(10)
      continue;
    for s in services:
      if debug: print "s:",s
      loc=s.split(',');
      if loc[0] == '':
        continue
      if debug: print "loc:",loc
      attr=subprocess.check_output(["slptool","findattrs",loc[0]]);
      host={}
      host['ip']=loc[0].split("//")[1]
      host['hasPanel']=False
      if attr.find("hasPanel") != -1:
        if debug: print "host has panel"
        host['hasPanel']=True
      if debug: print host
      hosts.append(host)
    if debug: print hosts
    tests=[]
    for i in range(0,2):
      n = random.randint(0,len(lines)-1)
      tests.append(lines[n])

    if debug: print tests[0],tests[1] #,tests[2]
    
    image_type = "Action"
    # you can change the query for the image  here  
    #query = "Terminator 3 Movie"
    #query= query.split()
    #query='+'.join(query)
    query=tests[0]+'+'+tests[1]
    url="http://www.google.com/images?q="+query

    #print url
    header = {'User-Agent': 'Mozilla/5.0'} 
    soup = get_soup(url,header)
    if 1:
      images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
      imageTotal=0
      for h in hosts:
        imageCount = 0
        while ( imageCount < maxImagesPerHost ):
          raw_img = urllib2.urlopen(images[imageTotal+imageCount]).read()
          imageCount += 1
          cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
          if debug: print cntr
          imgPath=DIR + '/' + image_type + "_"+ str(cntr)+".jpg"
          f = open(imgPath, 'wb')
          f.write(raw_img)
          f.close()
          flgPath=DIR + '/' + image_type + "_"+ str(cntr)+".flg"
          f = open(flgPath, 'w')
          f.close()
          textPath=None
          if h['hasPanel']:
            if debug: print "doing has panel"
            if imageCount == 1:
              textPath=DIR+"/newText.lkp"
              f = open(textPath,'w')
              f.write(tests[0]+'\n')
              f.write(tests[1]+'\n')
              f.close();
          if debug:
            print "h{'ip'}:",h['ip']
            print "imgPath:",imgPath
            print "flgPath:",flgPath
            if textPath is not None:
              print "textPath:",textPath
            print "imgCount:",imageCount
        imageTotal+=imageCount
        if debug: print "imageTotal:",imageTotal
    else:
      print soup
    time.sleep(60)

if __name__ == '__main__':
  imageLookup()
