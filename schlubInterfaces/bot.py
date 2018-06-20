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
import syslog
import requests
import json
import random
import datetime
import time
import math
import sqlite3
import atexit
from shutil import copyfile
from textblob import TextBlob
from textblob import Word


parrotUrl      = "http://192.168.0.103:8085/data"
schlubUrl      = "http://192.168.0.103:8080"
# words_filename     = "../lists/wordtank.json"
srt_filename       = "../lists/pos_untitled.json"
stopwords_filename = "../lists/stopwords.json"
sqlite_filename    = "../lists/words.db"


sql_conn = sqlite3.connect(sqlite_filename)
sql_c = sql_conn.cursor()

# utility convert u'blahblah' strings from unicode to ascii
def nu(s):
  return s.encode('ascii', 'ignore')

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
  # print(stopwords)
  print("stopwords length:", len(stopwords), "srt length:", len(srt))


# doesnt do sql COMMIT!!
def word2db(word, pos="NN", ts=-1, src="ip"):
  if ts < 0:  ts = time.time()
  print (word,pos,ts,src)
  try:
    sql =  "insert into word (w, pos, ts, src) values ('{}', '{}',{}, '{}'); "\
          .format(word,pos, ts, src)
    #print(sql)
    sql_c.execute(sql)
  except sqlite3.IntegrityError:  # constraint w, pos unique violated: UPDATE instead of INSERTing
    sql = "update word SET cnt = cnt+1, ts={} where w = '{}' and pos = '{}';".format(ts, word, pos)
    print("DUPLICATE: "+ word + ' ' + pos)
    sql_c.execute(sql)

def synonyms(theWord, thePOS='NN'):
  rv = []
  poscode = thePOS[0].lower()
  if poscode in ['a','n', 'v']:
    symsets = Word(theWord).lemmatize().get_synsets(pos=poscode)
    for ss in symsets:
      rv.extend(ss.lemma_names())
    print "synonyms of {} {}".format(theWord, rv)
  return rv

# load a whole phrase or text into word table of open words.db
def text2db(theText, ts=-1, src="ip", withSynonyms=False):

  if ts < 0: ts = time.time()

  text_tb = TextBlob(theText)
  #print text_tb

  for w in text_tb.tags:
    if not w[0].lower() in stopwords:
      word2db(w[0], w[1], ts, src)
      if withSynonyms:
       syns = synonyms(w[0], w[1])
       for s in syns:
         word2db(s, w[1], ts, 'ip-syn')


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

def utter():
  # get a srt phrase from the subtitle file
  srtlen = len(srt)
  theSRT = srt[random.randint(0, srtlen)]
  print "utter: srt len = {}".format(srtlen)
  print "srt = {}".format(theSRT)
  # get a bunch of recent words from the word db
  # substitute some words in the srt phrase
  # say it
  return

def byebye():
  sql_conn.close()
  # save updated json words database file.
  # write a backup of the old file before writing.

  # global words
  # copyfile(words_filename, words_filename + '.bu'+str(int(time.time())))
  # with open(words_filename, 'w') as outfile:  
  #   json.dump(words, outfile, indent=2)
  # print('updated wordtank', words)

  print("bot sez byebye")

atexit.register(byebye)

init_json()


if __name__ == '__main__':
  pname = sys.argv[0]
  syslog.syslog(pname+" started at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
  last_timestamp = 0 
  init_json()

  while True:
    transcript = hitParrot(0,last_timestamp)
    if len(transcript) > 0:
     last_timestamp = int(math.ceil(transcript[0]['timestamp']))
     print len(transcript)
     for x in transcript:
       thePhrase = x['trans'].strip()
       if x['confidence'] > 0.7:
        # say(thePhrase, "de")
         print(thePhrase)
       show(thePhrase)
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(2)


