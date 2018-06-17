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
import sqlite3
import atexit
from shutil import copyfile
from textblob import TextBlob

parrotUrl      = "http://192.168.0.105:8085/data"
schlubUrl      = "http://192.168.0.105:8080"

words_filename     = "../lists/wordtank.json"
srt_filename       = "../lists/pos_untitled.json"
stopwords_filename = "../lists/stopwords.json"
sqlite_filename    = "../lists/words.db"


sql_conn = sqlite3.connect(sqlite_filename)
sql_c = sql_conn.cursor()

def init_json():
  global srt, stopwords, words

  # load up 'database' dict objects from json files
  with open(srt_filename) as json_srt:               
    srt        = json.load(json_srt)
  with open(stopwords_filename) as json_stopwords:   
    stopwords  = json.load(json_stopwords)
  # with open(words_filename) as json_words:           
  #   words      = json.load(json_words)

  #test -- print out wordtank
  # print("words", words)
  print(stopwords)
  print("stopwords length:", len(stopwords), "srt length:", len(srt))


def ph2db(phrase, ts=time.time(), src="ip"):

  phrase_tb = TextBlob(phrase)
  print phrase_tb

  for w in phrase_tb.tags:
    if not w[0].lower() in stopwords:
      rv = (w[0], w[1], ts, src)
      print rv
      try:
        sql =  "insert into word (w, pos, ts, src) values ('{}', '{}',{}, '{}'); "\
              .format(w[0], w[1], ts, src)
        print(sql)
        sql_c.execute(sql)
      except sqlite3.IntegrityError:
        sql = "update word SET cnt = cnt+1, ts={} where w = '{}' and pos = '{}';".format(ts, w[0], w[1])
        print("CONFLICT: " + sql)
        sql_c.execute(sql)

      sql_conn.commit()



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
 
# low-level cmd to say a phrase using schlub server 
def say(phraseIn, langIn='en-au'):
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

def byebye():
  global words
  sql_conn.close()
  # save updated json words database file.
  # write a backup of the old file before writing.

  # copyfile(words_filename, words_filename + '.bu'+str(int(time.time())))
  # with open(words_filename, 'w') as outfile:  
  #   json.dump(words, outfile, indent=2)
  # print('updated wordtank', words)

  print("bot sez byebye")

atexit.register(byebye)

if __name__ == '__main__':
  last_timestamp = 0

  # test of words writing
  foo = 'NN'
  if not ('NN' in words) : words['NN'] = []
  words['NN'].append({"w": "added", "ts": time.time() })
 


  while True:
    # r = hitParrot(0,last_timestamp)
    # if len(r) > 0:
    #  last_timestamp = int(math.ceil(r[0]['timestamp']))
    # print len(r)
    # for x in r:
    #   thePhrase = x['trans'].strip()
    #   if x['confidence'] > 0.7:
    #     say(thePhrase, "de")
    #     print(thePhrase)
    #   show(thePhrase)
    print(words)
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(2)


