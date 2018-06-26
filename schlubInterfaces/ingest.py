#!/usr/bin/env/python

# ingest.py    june 2018  t perkis  for Darmstadt
#
#  cmd-lineable functions for  off-line ingestion of various datasources into sql database.
#

import dataio
import json
import time
import os
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# srt files that have had pos tags added can be read into the phrase table
def posJson2PhraseDB(filepath, srctag=""):
  if srctag == '':  
    srctag = os.path.basename(filepath)  # /foo/bar/quux.js -> quux.js
    srctag = os.path.splitext(srctag)[0] # quux.js -> 'quux'
  theTs = time.time()
  cnt = 0

  with open(filepath) as fp:  
   theJSON = fp.read()

  d = json.loads(theJSON)
  for r in d:
    scc = srctag + '-' + str(cnt)
    if cnt % 100 == 0:
      print(r['text'], r['tw'], scc)

    dataio.phrase2PhraseDB(r['text'], r['tw'], theTs, scc)
    cnt += 1

  print(cnt, "lines loaded.")
  dataio.sql_conn.commit()

def sentences2PhraseDB(filepath, srctag=''):
  # for a text file with one phrase per line, add pos and stuff in db phrase table.
  if srctag == '':  
    srctag = os.path.basename(filepath)  # /foo/bar/quux.js -> quux.js
    srctag = os.path.splitext(srctag)[0] # quux.js -> 'quux'
  dataio.file2PhraseDB(filepath, srctag)


if __name__ == '__main__':

  # posJson2PhraseDB(sys.argv[1], sys.argv[2])

  sentences2PhraseDB(sys.argv[1], sys.argv[2])




