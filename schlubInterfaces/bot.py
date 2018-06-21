#!/usr/bin/env python


# bot.py     perkis june 2018 for Darmstadt
#
#     * iParrot.py is listening and queuing up transcripts of google-interpreted voice input, available on a http server
#     * bot.hitParrot() grabs data from this server.
#     * bot.text2db()  takes any phrase/short text and ingests the words in it into the word database (sqlite)
#     * bot.word2db() is called by above to write individual words to db with pos taggin
#     * bot.file2db() will ingest a given text file into the word database w repeated calls to text2db for each line.
#     * bot.srt is a dict loaded up with lines of film subtitle utterances
#     * bot.getwords retrieves word lists from the word database
#     * bot.synonyms() uses wordnet to get synotnyms of a given (pos-tagged) word
#     * bot.say(), bot.show(), bot.soundVol() are low level cmd-senders to schlub.py server
#     * bot.utter() grabs a subtitle line and some words from the word.db, munges them together and speaks the result.
#     * bot.updateWords() uses hitParrot() and text2db() to load recently said things by users into word db
#
#     So basically updateWords() and utter() comprise a full pipeline: reading user utterances, saving the words, and generating
#     new utterances by our arty bot entity.

# on exit persist the wordlist to a file, and read it in on startup


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

parrotUrl      = "http://192.168.0.110:8085/data"
schlubUrl      = "http://192.168.0.110:8080"
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


# get n words from db filtered by given pos tag or tags.
#  usage: getwords(5, 'NN', 'NP' <etc>)
def getwords(n=1, *arg): 
  sql = "select w, pos from word "
  if len(arg) > 0:
    sql += "where pos in {} ".format(arg)
  # sql += "order by ts desc limit {};".format(n)
  sql += "order by RANDOM() limit {};".format(n) # for now.. eventually use newest
  # print(sql)
  sql_c.execute(sql)
  return sql_c.fetchall()


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
      word2db(w[0].lower(), w[1], ts, src)
      if withSynonyms:
       syns = synonyms(w[0], w[1])
       for s in syns:
         word2db(s, w[1], ts, 'ip-syn')


  sql_conn.commit()

# ingest a text file into open words.db
def file2db(fname, src):
  with open(fname) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       if len(line) > 5:
         try:
          text2db(line.strip(), -1, src)
          if cnt % 50 == 0:
            print(" {}".format(cnt))
         except:
          print("error reading line ", cnt)
       line = fp.readline()
       cnt += 1

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
 
# for convenience, some schlub commands: 
# low-level cmd to say a phrase using schlub server 
def say(phraseIn, langIn='en-au'):
  theData = {"cmd": "Phrase", "args": { "phrase": phraseIn, "reps": 1, "lang": langIn}}
  r = requests.post(schlubUrl, data=json.dumps(theData))
  print r

# show a sentence on screen
def show(phraseIn):
  theData = {"cmd": "Show", "args": { "phrase": phraseIn}}
  r = requests.post(schlubUrl, data=json.dumps(theData))

def soundVol(volIn):
  theData = {"cmd": "SoundVol", "args": [volIn]}
  r = requests.post(schlubUrl, data=json.dumps(theData))
  print r

def utter(langIn='en-au'):
  # get a srt phrase from the subtitle file
  srtlen = len(srt)
  theSRT = srt[random.randint(0, srtlen)]
  print "utter: srt len = {}".format(srtlen)
  print "srt = {}".format(theSRT)
  # get a bunch of recent words from the word db
  someNouns =  getwords(20, 'NN', 'NP', 'NS')
  print("someNouns: {}".format(someNouns))

  # substitute some words in the srt phrase
  rv = []
  for w in theSRT['tw']:
    if w[1] in ['NN', 'NNP', 'NNS']:
      rv.append(someNouns.pop()[0])
    else:
     rv.append(w[0])
  # print rv
  rvs = ' '.join(rv).strip().replace('.','').replace(" ' ","'").replace("_"," ")
  print(rvs)
  say(rvs,langIn)

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
         say(thePhrase, default_voice )
         print(thePhrase)
       show(thePhrase)
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(2)


