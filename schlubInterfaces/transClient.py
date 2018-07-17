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
import host
sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
sys.path.append(home+"/GitProjects/artDisplay/schlub")
import slp

dataBufSize = 20
dataBuf = []
displayList = []
fullList=[]

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
  print "getting host list"
  hosts = host.getHosts()
  print hosts
  transServerIp = sys.argv[1]
  if len(sys.argv) > 2:
    confidence = sys.argv[2]
  else:
    confidence = 5
  print "trans server ip:", transServerIp;
  testIp = transServerIp.split(':')[0]
  #url = "http://"+transServerIp+"/data?ct=5"
  url = "http://"+transServerIp+"/data?ct="+str(confidence)
  print "url",url 
  for h in hosts:
    if h['ip'] == testIp:
      continue
    resp = sendToHost(h['ip'],{'cmd' : 'Probe', 'args' : [""] })
    fullList.insert(0,h['ip'])
    if resp['hasScreen']:
      print "ip:",h['ip'],"display enabled"
      displayList.insert(0,h['ip'])
  print
  for d in displayList:
    print d
  while True:
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
    print "phrase count:",len(dataBuf),"index:",index
    if len(dataBuf) < 2:
      continue
    f = random.choose(fullList)
    d = random.choose(displayList)
    args = {}
    args['phrase'] = dataBuf[index]['trans']
    resp = sendToHost(d['ip'],{'cmd' : 'Show', 'args' : args })
    print resp
    index += 1
    args['phrase'] = dataBuf[index]['trans']
    args['reps'] = 1
    resp = sendToHost(f['ip'],{'cmd' : 'Phrase','args' : args})
    print resp

    index += 1
    time.sleep(1)



