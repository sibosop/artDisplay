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
import traceback
import ssl
import fehtest
import datetime
import signal

debug=False
imageDebug=False
copyDebug=False
slpDebug=False

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


def getRawImage(image):
  if imageDebug: print "image:",image
  imageTypes=['full','thumb']
  raw_img=None
  for t in imageTypes: 
    try:
      startTime = time.time()
      if imageDebug: print "open image type",t,"image:",image[t]
      req = urllib2.Request(image[t],headers={'User-Agent' : "Magic Browser"})
      gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
      con = urllib2.urlopen( req, context=gcontext )
      raw_img = con.read()
      #raw_img = urllib2.urlopen(images[imageIndex]).read()
      if imageDebug: print "elapsed:",time.time() - startTime
      tmpPath = "/tmp/fehTest.jpg"
      f = open(tmpPath, 'wb')
      f.write(raw_img)
      f.close()
      if fehtest.fehTest(tmpPath) != 0:
        print "feh fails for ",image[t]
        continue;
      else:
        if imageDebug: print "feh test good for",image[t]
      break;
    except:
      syslog.syslog("return from exception for type "
                            +t+" image: "+image[t])
      syslog.syslog("elapsed:"+str(time.time() - startTime))
      syslog.syslog(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
      syslog.syslog(traceback.format_exc())
      continue;
  return raw_img 
    

#@profile
def imageLookupLoop():
  cacheDir = adGlobal.cacheDir;
  image_type = "Action"
  maxImagesPerHost = 5
  syslog.syslog("search method: "+adGlobal.searchType)
  hosts=[]
  services = subprocess.check_output(["slptool","findsrvs","service:artdisplay.x"]).split('\n');
  if len(services) == 0:
    syslog.syslog("no available services")
    return
  for s in services:
    if slpDebug: print "s:",s
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
  if slpDebug: print "hosts:",str(hosts)
  images=[]
  choices=[]
  if adGlobal.searchType == "Archive":
    vars=archive.getArchive();
    images=vars[0]
    choices=vars[1]
  else:
    while len(images) < 20:
      images=[]
      choices=[]
      choices = words.getWords()
      images = scraper.scraper(choices[:])
  syslog.syslog("select: "+choices[0]+" "+choices[1])
  copyList = {}
  for h in hosts:
    copyList[h['ip']] = {}
    copyList[h['ip']]['image'] = []
    copyList[h['ip']]['flag'] = []
    copyList[h['ip']]['text'] = None
    if h['hasPanel']:
      if debug: print "doing has panel"
      if len(choices) < 2:
        syslog.syslog("WARNING, choices array not loaded")
      else: 
        textPath=cacheDir+"/"+adGlobal.textName
        f = open(textPath,'w')
        f.write(choices[0]+'\n')
        f.write(choices[1]+'\n')
        f.close();
        copyList[h['ip']]['text']=textPath 
        if debug: print "textPath:",textPath

  hostCount=0
  for image in images:
    if ( adGlobal.searchType != "Archive"):
      raw_img=getRawImage(image)
      if raw_img is None:
        print "raw_image = none",image
        continue;
      cntr = len([i for i in os.listdir(cacheDir) if image_type in i]) + 1
      if debug: print cntr
      imgPath=cacheDir + '/' + image_type + "_"+ str(cntr)+".jpg"
      f = open(imgPath, 'wb')
      f.write(raw_img)
      f.close()
      flgPath=cacheDir + '/' + image_type + "_"+ str(cntr)+".flg"
      f = open(flgPath, 'w')
      f.close()
      del raw_img
    else:
      try:
        cmd=["cp",image,cacheDir]
        if debug: print "cmd",cmd
        subprocess.check_output(cmd)
        imgPath=cacheDir+"/"+os.path.basename(image)
        i=os.path.basename(image)
        flgPath=cacheDir+"/"+image[:image.rindex(".")]+".flg"
        cmd=["touch",flgPath]
        if debug: print "cmd",cmd
        subprocess.check_output(cmd)
      except subprocess.CalledProcessError, e:
        syslog.syslog("archive file copy problem: "+', '.join(cmd)+str(e.output))
        continue;

    if imageDebug:  print "imgPath:",imgPath,"to host",hostCount,"-",hosts[hostCount]['ip']
    if imageDebug: print "flgPath:",flgPath,"to host",hostCount,"-",hosts[hostCount]['ip']
    copyList[hosts[hostCount]['ip']]['image'].append(imgPath)
    copyList[hosts[hostCount]['ip']]['flag'].append(flgPath)
    hostCount += 1
    if hostCount == len(hosts):
      hostCount=0

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
      if debug: print "cmd afer set to cv:",cmd,"cv:",cv
      for i in copyList[ip]['image']:
        cmd.append(i)
      cmd.append(dest)
      if copyDebug: print "file copy:",str(cmd)
      subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
      syslog.syslog("file copy problem: "+', '.join(cmd)+str(e.output))
      continue
      
  for ip in copyList.keys():
    try:
      cv=getCmdVars(ip)
      dest=getDest(ip)
      cmd=[]
      cmd=cv[:]
      if debug: print "cmd afer set to cv:",cmd
      for i in copyList[ip]['flag']:
          cmd.append(i)
      cmd.append(dest)
      if copyDebug: print "flag copy cmd:",str(cmd)
      subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
      print "file copy problem: ",str(cmd),str(e.output)
      continue  
      
  for ip in copyList.keys():
    try:
      cv=getCmdVars(ip)
      dest=getDest(ip)
      cmd=[]
      cmd=cv[:]
      if copyList[ip]['text'] is not None:
        cmd.append(copyList[ip]['text'])
        cmd.append(dest)
        if copyDebug: print "text copy cmd:",str(cmd)
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
      syslog.syslog("file copy problem: "+', '.join(cmd)+str(e.output))
      continue

  if adGlobal.searchType != "Archive":
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
      syslog.syslog("doing archive")
      subprocess.check_output(cmd)
      syslog.syslog("archive complete")
    except subprocess.CalledProcessError, e:
      syslog.syslog("archive problem: "+', '.join(cmd)+str(e.output))
      
  files = glob.glob(cacheDir+"/*")
  if debug: print "removing:",files
  for f in files:
      if f == cacheDir+"/placeholder":
        continue
      os.remove(f)

def imageLookup():
  loopStart= time.time()
  while True:
    signal.alarm(600)
    syslog.syslog("ImageLookup Loop Time "+str(time.time()-loopStart))
    loopStart=time.time()
    imageLookupLoop()
    time.sleep(30)

if __name__ == '__main__':
  imageLookupLoop()
