#!/usr/bin/env python


# schlubbot.py     perkis june 2018 for Darmstadt
#
# in a loop:
#  hitParrot, getting all (ct=0) transcript records since last hit (keep a timestamp variable)
#     process the records into a wordlist, keyed by POS and sorted by timestamp.
# every now and then, say something:
#     get a srt line from the srt_obj
#     substitute some of the nouns and verbs in the sentence with nouns or verbs from the wordlist
#     tell schlub to say it
# 
# on exit persist the wordlist to a file, and read it in on startup (NIY)


import sys
import requests
import json
import random
import time
import math

from textblob import TextBlob

parrotUrl = "http://192.168.0.105:8085/data"
schlubUrl = "http://192.168.0.105:8080"

srt_f = open("../lists/pos_all_srt.json","r")
srt_json = srt_f.read()
srt_obj = json.loads(srt_json)

# conf  0-9 (minimum confidence), timestamp = minimum timestamp
def hitParrot(conf=0, timestamp=0):
  url = parrotUrl+"?ct="+str(conf)
  if timestamp > 0:
    url += "&ts="+str(timestamp)
  # print("url:"+url)
  r = requests.get(url)
  rv = r.json()
  if rv['status'] == "ok":
    return rv['transcript']
  else:
    return r.status_code
 
def say(phraseIn, langIn='en-aus'):
  theData = {"cmd": "Phrase", "args": { "phrase": phraseIn, "reps": 1, "lang": langIn}}
  r = requests.post(schlubUrl, data=json.dumps(theData))

def show(phraseIn):
  theData = {"cmd": "Show", "args": { "phrase": phraseIn}}
  r = requests.post(schlubUrl, data=json.dumps(theData))


def mangle(phrase):
   phrase_tb = TextBlob(phrase)
   ph_tags = phrase_tb.tags
   srt = srt_obj[random.randint(0,len(srt_obj))]
   print srt['tw']
   print ph_tags
   # get random srt phrase, and for each word, replace word with word from same position in input phrase
   #  ONLY if it has the same part of speech
   rv = []

   for i in range( 0,len(srt['tw'])):
    try:
      if ph_tags[i][1] == srt['tw'][i][1]:
        rv.append(ph_tags[i][0])
      else:
        rv.append(srt['tw'][i][0])
    except:
       rv.append(srt['tw'][i][0])

   return ' '.join(rv).replace(" ' ","'").replace(" .",".")


if __name__ == '__main__':
  last_timestamp = 0
  while True:
    r = hitParrot(0,last_timestamp)
    if len(r) > 0:
     last_timestamp = int(math.ceil(r[0]['timestamp']))
    print len(r)
    for x in r:
      thePhrase = x['trans'].strip()
      if x['confidence'] > 0.7:
        say(thePhrase, "de")
        print(thePhrase)
      show(thePhrase)
    time.sleep(2)

