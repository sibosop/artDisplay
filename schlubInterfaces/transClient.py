#!/usr/bin/env python
import os
home = os.environ['HOME']
import sys
import syslog
import datetime
import time
import urllib2
import json
import os
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import slp
import schlubcmd
import mangle

dataBufSize = 20
dataBuf = []
displayList = []

def sendToHost(ip,cmd):
  print "send to host:",ip,cmd
  url = "http://"+ip+":8080"
  print("url:"+url)
  print("cmd json:"+json.dumps(cmd))
  req = urllib2.Request(url
              ,json.dumps(cmd),{'Content-Type': 'application/json'})
  f = urllib2.urlopen(req)
  test = f.read()
  print("got response:"+test)
  return json.loads(test)

if __name__ == '__main__':
  run=True
  checkDisplay = False
  if len(sys.argv) > 2:
    if sys.argv[2] == "-d":
      checkDisplay = True
  print "getting host list"
  schlubcmd.getHostList()
  schlubcmd.printHostList()
  transServerIp = sys.argv[1]
  print "trans server ip:", transServerIp;
  #url = "http://"+transServerIp+"/data?ct=5"
  url = "http://"+transServerIp+"/data?ct=0"
  print "url",url 
  for h in schlubcmd.hosts:
    resp = sendToHost(h['ip'],{'cmd' : 'Probe', 'args' : [""] })
    if checkDisplay:
      if resp['displayEnabled']:
        print "ip:",h['ip'],"display enabled"
        displayList.insert(0,h['ip'])
    else:
      print "ip:",h['ip'],"display enabled"
      displayList.insert(0,h['ip'])
  print
  for d in displayList:
    print d
  print

  while run:
    print "url:",url
    response = urllib2.urlopen(url)
    html = response.read()
    data = json.loads(html)
    for t in data['transcript']:
      if len(dataBuf) == 0:
        dataBuf.insert(0,t)
      else: 
        if float(t['timestamp']) > dataBuf[0]['timestamp']:
          dataBuf.insert(0,t)
      if len(dataBuf) >= dataBufSize:
        dataBuf.pop()
    for t in dataBuf:
      print t
    print

    index = 0
    for ip in displayList:
      print len(dataBuf),index
      if len(dataBuf) > index:
        phrase = dataBuf[index]['trans']
        args = {}
        args['phrase'] = mangle.mangle.py
        resp = sendToHost(ip,{'cmd' : 'Show', 'args' : args })
      index += 1
      
      
    time.sleep(1)



