#!/usr/bin/env python
import os
import random
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import time





def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)), "html5lib")
  #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url)), "html.parser")


def imageLookup():
    #print "hello world"
  
    DIR = os.environ.get('ID_CACHE');
    if DIR is None:
      print "Error: ID_CACHE not defined"
      exit(-1)
    print DIR
    wordFile = os.environ.get('WORDS');
    if wordFile is None:
      print "Error: WORDS not defined"
      exit(-1)
    maxImages = 6
    while True:
      lines = open(wordFile).read().split('\n')
      #print "number of words",len(lines)


      tests=[]
      for i in range(0,2):
        n = random.randint(0,len(lines)-1)
        tests.append(lines[n])

      print tests[0],tests[1] #,tests[2]
    
  

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
        imgCount = 0
        images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
        #print images
        for img in images:
          #print img
          if ( imgCount < maxImages ):
            imgCount += 1
            raw_img = urllib2.urlopen(img).read()
            cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
            #print cntr
            f = open(DIR + '/' + image_type + "_"+ str(cntr)+".jpg", 'wb')
            f.write(raw_img)
            f.close()
            f = open(DIR + '/' + image_type + "_"+ str(cntr)+".flg", 'w')
            f.close()
        if imgCount > 0:
          f = open(DIR + '/newText.lkp','w');
          f.write(tests[0]+'\n');
          f.write(tests[1]+'\n');
          f.close();
      else:
        print soup
      time.sleep(60)
    

if __name__ == '__main__':
  imageLookup()