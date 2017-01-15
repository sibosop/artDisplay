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
import inspect


debug=False
hangDebug=True;
imageDebug=False
copyDebug=False
slpDebug=True

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
      adGlobal.mutex.acquire()
      f = open(tmpPath, 'wb')
      f.write(raw_img)
      f.close()
      adGlobal.mutex.release()
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
      adGlobal.mutex.release()
      continue;
    finally:
      adGlobal.mutex.release()
  return raw_img 
    

#@profile
def imageLookupLoop():
  cacheDir = adGlobal.cacheDir;
  image_type = "Action"
  maxImagesPerHost = 5
  searchType = adGlobal.searchType
  syslog.syslog("search method: "+searchType)
  if hangDebug: syslog.syslog("Hang debug:"
		+__file__+" "
		+str(inspect.currentframe().f_lineno))
  hosts=[]

  services = subprocess.check_output(["slptool","findsrvs","service:artdisplay.x"]).split('\n');
  if len(services) == 0:
    syslog.syslog("no available services")
    return
  for s in services:
    if hangDebug: syslog.syslog("Hang debug:"
      +__file__+" "
      +str(inspect.currentframe().f_lineno))
    if slpDebug: syslog.syslog("slp s:"+s)
    loc=s.split(',');
    if loc[0] == '':
      continue
    if slpDebug: syslog.syslog("loc:"+str(loc))
    if hangDebug: syslog.syslog("Hang debug:"
      +__file__+" "
      +str(inspect.currentframe().f_lineno))
    attr=subprocess.check_output(["slptool","findattrs",loc[0]]);
    host={}
    host['ip']=loc[0].split("//")[1]
    host['hasPanel']=False
    if attr.find("hasPanel") != -1:
      if slpDebug: syslog.syslog(str(host)+"host has panel");
      host['hasPanel']=True
    if slpDebug: syslog.syslog("slp host"+str(host))
    hosts.append(host)
  if slpDebug: syslog.syslog("hosts:"+str(hosts))
  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
  images=[]
  choices=[]
  if searchType == "Archive":
    if hangDebug: syslog.syslog("Hang debug:"
      +__file__+" "
      +str(inspect.currentframe().f_lineno))
    vars=archive.getArchive();
    images=vars[0]
    choices=vars[1]
    if hangDebug: syslog.syslog("Hang debug:"
      +__file__+" "
      +str(inspect.currentframe().f_lineno))
  else:
    while len(images) < 20:
      images=[]
      choices=[]
      choices = words.getWords()
      images = scraper.scraper(choices[:])
      if len(images) == 1 and images[0] == "error":
        return
  syslog.syslog("select: "+choices[0]+" "+choices[1])
  copyList = {}
  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
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
        adGlobal.mutex.acquire()
        f = open(textPath,'w')
        f.write(choices[0]+'\n')
        f.write(choices[1]+'\n')
        f.close();
        adGlobal.mutex.release()
        copyList[h['ip']]['text']=textPath 
        if debug: print "textPath:",textPath

  hostCount=0
  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
  for image in images:
    if ( searchType != "Archive"):
      if hangDebug: syslog.syslog("Hang debug:"
        +__file__+" "
        +str(inspect.currentframe().f_lineno))
      raw_img=getRawImage(image)
      if hangDebug: syslog.syslog("Hang debug:"
        +__file__+" "
        +str(inspect.currentframe().f_lineno))
      if raw_img is None:
        print "raw_image = none",image
        continue;
      adGlobal.mutex.acquire()
      cntr = len([i for i in os.listdir(cacheDir) if image_type in i]) + 1
      adGlobal.mutex.release()
      if debug: print cntr
      imgPath=cacheDir + '/' + image_type + "_"+ str(cntr)+".jpg"
      adGlobal.mutex.acquire()
      f = open(imgPath, 'wb')
      f.write(raw_img)
      f.close()
      flgPath=cacheDir + '/' + image_type + "_"+ str(cntr)+".flg"
      f = open(flgPath, 'w')
      f.close()
      adGlobal.mutex.release()
      del raw_img
    else:
      adGlobal.mutex.acquire()
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
        adGlobal.mutex.release()
        continue;
      finally:
        adGlobal.mutex.release()

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
      
  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
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

  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
  for ip in copyList.keys():
    try:
      login = "pi@"+ip
      if adGlobal.isLocalHost(ip):
        cmd = ["touch",adGlobal.timeStampFile]
      else:
        cmd=["ssh",ip,"touch",adGlobal.timeStampFile]
      if debug: syslog.syslog("sending cmd:"+str(cmd));
      subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
      syslog.syslog("timestamp set problem: "+', '.join(cmd)+str(e.output))
      continue
      
  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
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
      
  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
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

  

  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
  if ((searchType != "Archive") and adGlobal.doArchive ):
    if debug: print "archiving cacheDir"
    adGlobal.mutex.acquire()
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
    finally:
      adGlobal.mutex.release()
      
      
  if hangDebug: syslog.syslog("Hang debug:"
    +__file__+" "
    +str(inspect.currentframe().f_lineno))
  files = glob.glob(cacheDir+"/*")
  if debug: print "removing:",files
  for f in files:
      if f == cacheDir+"/placeholder":
        continue
      os.remove(f)

def imageLookup():
  loopStart= time.time()
  while True:
    signal.alarm(300)
    syslog.syslog("ImageLookup Loop Time "+str(time.time()-loopStart))
    loopStart=time.time()
    imageLookupLoop()
    sleepTime = 30
    time.sleep(sleepTime)

if __name__ == '__main__':
  imageLookupLoop()
