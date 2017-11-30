#!/usr/bin/env python
import os
import roman
import json
home = os.environ['HOME']
import sys
import syslog
import threading
import shakes
import emily
import browning
import shutil

sys.path.append(home+"/GitProjects/artDisplay/imageLookup")
import textSpeaker

def compilePoem(poem):
  rval = []
  print("compile poem")
  count = 0
  try:
    for l in poem:
      count += 1
      print "line", l
      if l == "+++++":
        sound = None
      else:
        file = None
        while file is None:
          file = textSpeaker.makeSpeakFile(l)
      entry = {}
      entry['text'] = l
      if ( l == "+++++"):
        entry['file'] = "None" 
      else:
        dirPath = os.path.dirname(file)
        newFileName = dirPath+"/line"+str(count)+".wav"
        os.rename(file,newFileName)
        entry['file'] = newFileName
      rval.append(entry);
  except Exception as e:
    print("compile poem: "+str(e))
    rval = []
  return rval

def checkBase(author):
  baseDir = os.environ['POEM_DIR']
  dirName = baseDir + "/" + author
  print "dirName:",dirName
  if ( os.path.exists(dirName) and  os.path.isdir(dirName) == False ):
      print "NON DIRECTORY PATH:",dirName
      exit(-1)
  if ( os.path.exists(dirName) == False ):
    print "creating:",dirName
    os.mkdir(dirName)
  return dirName

def convertPoem(author,data,num):
  baseDir = checkBase(author)
  line = 0
  poem = []
  poemDir=baseDir+"/poem"+str(num)
  if ( os.path.exists(poemDir) == False ):
    os.mkdir(poemDir)
  for l in data:
    line += 1
    entry = {}
    fname = l['file']
    if fname == "None":
      destName = "None"
    else:
      destName = "line"+str(line)+".wav"
      dest = poemDir+"/"+destName
      print "mv",fname,"to",dest
      shutil.move(fname,dest)

    entry['text'] = l['text']
    entry['file'] = destName
    poem.append(entry)

  jsonStr = json.dumps(poem)
  print jsonStr
  poemFile = open(poemDir+"/data.txt","w")
  poemFile.write(jsonStr)
  poemFile.write("\n")
  poemFile.close()
    
#cols = [shakes,emily,browning]
cols = [emily,browning]
    
if __name__ == '__main__':
  for c in cols:
    for i in range(c.getMinPoem(),c.getNumPoems()+1):
      entry  = c.create(i)
      data = compilePoem(entry)
      convertPoem(c.getId(),data,i)
