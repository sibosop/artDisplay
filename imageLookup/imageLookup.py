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
import scraper
import words
import sys
import uuid
import archive

debug=False


def getCmdVars(ip):
  cmdVars = []
  if adGlobal.isLocalHost(ip):
    cmdVars.append("cp")  
  else:
    cmdVars.append("scp")
    cmdVars.append("-q")
    cmdVars.append("-B")
  return cmdVars;
  
def getDest(ip):
  dest=None
  if adGlobal.isLocalHost(ip):
    dest = adGlobal.imageDir
  else:
    dest = "pi@"+ip+":"+adGlobal.imageDest
  return dest

def imageLookup():
  cacheDir = adGlobal.cacheDir;
  image_type = "Action"
  maxImagesPerHost = 4
  wds=words;
  syslog.syslog("search method: "+adGlobal.searchType)
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
    images=[]
    choices=[]
    if adGlobal.searchType == "Archive":
      vars=archive.getArchive();
      images=vars[0]
      choices=vars[1]
    else:
      w=words.Words()
      while len(images) < 20:
        choices = w.getWords()
        sc=choices[:]
        images = scraper.scraper(sc)
    imageIndex = 0
    copyList = {}
    for h in hosts:
      copyList[h['ip']] = {}
      copyList[h['ip']]['image'] = []
      copyList[h['ip']]['flag'] = []
      copyList[h['ip']]['text'] = None
      hostCount=0
      while ( hostCount < maxImagesPerHost ):
        if imageIndex >= len(images):
          if debug: print "not enough images for all hosts img total img index:",len(images),imageIndex
          break; 
        if debug: print "open image:",images[imageIndex]
        if ( adGlobal.searchType != "Archive"):
          try:
            raw_img = urllib2.urlopen(images[imageIndex]).read()
          except:
            e = sys.exc_info()[0]
            syslog.syslog("return from exception "+str(e))
            imageIndex += 1
            continue;
          imageIndex += 1
          hostCount += 1
          cntr = len([i for i in os.listdir(cacheDir) if image_type in i]) + 1
          if debug: print cntr
          imgPath=cacheDir + '/' + image_type + "_"+ str(cntr)+".jpg"
          f = open(imgPath, 'wb')
          f.write(raw_img)
          f.close()
          flgPath=cacheDir + '/' + image_type + "_"+ str(cntr)+".flg"
          f = open(flgPath, 'w')
          f.close()
        else:
          try:
            i = images[imageIndex]
            cmd=["cp",i,cacheDir]
            if debug: print "cmd",cmd
            subprocess.check_output(cmd)
            imgPath=cacheDir+"/"+os.path.basename(i)
            i=os.path.basename(i)
            flgPath=cacheDir+"/"+i[:i.rindex(".")]+".flg"
            cmd=["touch",flgPath]
            if debug: print "cmd",cmd
            subprocess.check_output(cmd)
          except subprocess.CalledProcessError, e:
            syslog.syslog("file copy problem: "+', '.join(cmd)+str(e.output))
            exit(-1)
          imageIndex+=1
          hostCount+=1
        textPath=None
        if h['hasPanel']:
          if debug: print "doing has panel"
          if hostCount == 1:
            if len(choices) < 2:
              syslog.syslog("WARNING, choices array not loaded")
            else: 
              textPath=cacheDir+"/"+adGlobal.textName
              f = open(textPath,'w')
              f.write(choices[0]+'\n')
              f.write(choices[1]+'\n')
              f.close();
              copyList[h['ip']]['text']=textPath 
        if debug:
          print "h{'ip'}:",h['ip']
          print "imgPath:",imgPath
          print "flgPath:",flgPath
          print "textPath:",textPath
          print "hostCount:",hostCount
        copyList[h['ip']]['image'].append(imgPath)
        copyList[h['ip']]['flag'].append(flgPath)

      if debug:
        for ip in copyList.keys():
          print "ip:",ip
          for i in copyList[ip]['image']:
            print "\timg:",i
          for i in copyList[ip]['flag']:
            print "\tflag:",i
          print "\ttext:",copyList[ip]['text']
      for ip in copyList.keys():
        cmd=[]
        try:
          cv=getCmdVars(ip)
          dest=getDest(ip)
          cmd=cv[:]
          if copyList[ip]['text'] is not None:
            cmd.append(copyList[ip]['text'])
            cmd.append(dest)
            if debug: print "cmd:",cmd
            subprocess.check_output(cmd)
          cmd=[]
          cmd=cv[:]
          if debug: print "cmd afer set to cv:",cmd,"cv:",cv
          for i in copyList[ip]['image']:
            cmd.append(i)
          cmd.append(dest)
          if debug: print "cmd:",cmd
          subprocess.check_output(cmd)
          cmd=[]
          cmd=cv[:]
          if debug: print "cmd afer set to cv:",cmd
          for i in copyList[ip]['flag']:
              cmd.append(i)
          cmd.append(dest)
          if debug: print "cmd:",cmd
          subprocess.check_output(cmd)
        except subprocess.CalledProcessError, e:
          syslog.syslog("file copy problem: "+', '.join(cmd)+str(e.output))
          continue
    if adGlobal.searchType == "Bing":
      if debug: print "archiving cacheDir"
      try:
        tmpFile="/tmp/tarFiles";
        f = open(tmpFile,"w");
        afiles=glob.glob(cacheDir+"/*.jpg")
        for af in afiles:
          fb=os.path.basename(af)
          f.write(fb+"\n");
        afiles=glob.glob(cacheDir+"/*.lkp")
        for af in afiles:
          fb=os.path.basename(af)
          f.write(fb+"\n");
        f.close()
        cmd = ["tar","-czf",adGlobal.archiveDir+"/"+str(uuid.uuid4())+".tgz","-C",cacheDir,"-T",tmpFile]
        if debug: print "cmd:",cmd
        subprocess.check_output(cmd)
      except subprocess.CalledProcessError, e:
        syslog.syslog("archive problem: "+', '.join(cmd)+str(e.output))
        
    files = glob.glob(cacheDir+"/*")
    if debug: print "removing:",files
    for f in files:
        if f == cacheDir+"/placeholder":
          continue
        os.remove(f)
    time.sleep(30)

if __name__ == '__main__':
  imageLookup()
