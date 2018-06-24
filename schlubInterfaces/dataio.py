#!/usr/bin/env python


# dataio.py     perkis june 2018 for Darmstadt
#
#   Set of dataio routines to read/write data to/from various components of the schlubBot universe.
#     * dataio.hitParrot() grabs data from the iParrot transServer [ DEPRECATED]
#     * dataio.text2WordDB()  takes any phrase/short text and ingests the words in it into the word database (sqlite)
#     * dataio.word2db() is called by above to write individual words to db with pos taggin
#     * dataio.file2db() will ingest a given text file into the word database w repeated calls to text2WordDB for each line.
#     * dataio.srt is a dict loaded up with lines of film subtitle utterances [DEPRECATED, ingest into sqlite phrase tbl]
#     * dataio.getwords() retrieves word lists from the words database word table
#     * dataio.synonyms() uses wordnet to get synotnyms of a given (pos-tagged) word
#     * dataio.datamuse() uses the datamuse.com api to get related words to a given word.
#     * dataio.say(), dataio.show(), dataio.soundVol() are low level cmd-senders to schlub.py server
#     * dataio.utter() grabs a subtitle line and some words from the word.db, munges them together and speaks the result.
#     * dataio.updateWords() uses hitParrot() and text2WordDB() to load recently said things by users into word db [DEPRECATED, 
#         iParrot should do this directly itself. ]
#
#     So basically updateWords() and utter() comprise a full pipeline: reading user utterances, saving the words, and generating
#     new utterances by our arty bot entity.

# on exit persist the wordlist to a file, and read it in on startup


import sys
reload(sys)
sys.setdefaultencoding('utf8')
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

parrotUrl   = "http://192.168.0.110:8085/data"
schlubUrls  = ["http://192.168.0.110:8080"]
wordsUrl    = "http://127.0.0.1:8081" 
datamuseUrl = "http://api.datamuse.com/words"

# words_filename     = "../lists/wordtank.json"
srt_filename       = "../lists/pos_untitled.json" # DEPRECATED, to be ingested into sqlite phrase table.
stopwords_filename = "../lists/stopwords.json"
sqlite_filename    = "../lists/words.db"
voices = ['en-au', 'en-uk', 'en', 'de']
default_voice = 'en-au'


sql_conn = sqlite3.connect(sqlite_filename)
sql_c = sql_conn.cursor()

# utility convert u'blahblah' strings from unicode to ascii
def nu(s):
  return s.encode('ascii', 'ignore')

def setSchlubUrls(arrIn):
  global schlubUrls
  schlubUrls = arrIn

def setParrotUrl(urlIn):
  global parrotUrl
  parrotUrl = urlIn

def init():
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
  sql_c.execute("select count() from word;")
  print("words in database: {}".format(sql_c.fetchone()[0]))


# get n words from db filtered by given pos tag or tags.
# used mostly by http word server
# (a bot analysis app will probably access worddb through transServer /words endpoint)
# posIn is a space-delimited set of POS tags like 'NN JJ NNS'
def getWordsDb(nnew= 10, nrand=10, posIn=''):  
  sqlnew = "select w, pos, ts from word "
  if len(posIn) > 0:
    pos =  "'" + posIn.replace(' ', "','") + "'"
    sqlnew += "where pos in ({}) ".format(pos)
  sqlnew += "order by ts desc limit {};".format(nnew)
  print(sqlnew)

  sqlrand = "select w, pos, ts from word "
  if len(posIn) > 0:
    pos =  "'" + posIn.replace(' ', "','") + "'"
    sqlrand += "where pos in ({}) ".format(pos)
  sqlrand += "order by RANDOM() limit {};".format(nrand) 
  print(sqlrand)

  sql_c.execute(sqlnew)
  newWds = list(sql_c.fetchall())

  sql_c.execute(sqlrand)
  randWds = list(sql_c.fetchall())

  rv = newWds + randWds
  random.shuffle(rv)
  print("getWordsDB rv ", rv)
  return(rv)

def getPhraseDb(): # for now just one at random
  sql = "select * from phrase order by RANDOM() LIMIT 1;"
  sql_c.execute(sql)
  return sql_c.fetchone()

def getWordsHTTP(nnew=10, nrand=10, pos=''):
  if len(pos) > 0:
    pos = pos.replace(' ', '+')
    req = wordsUrl+'/words?n='+str(nnew)+'&r='+str(nrand)+'&pos='+pos
    #print req
    rv = requests.get(req)
  else:
    req = wordsUrl+'/words?n='+str(nnew)+'&r='+str(nrand)
    #print req
    rv = requests.get(req)

  return json.loads(rv)

def getPhraseHTTP(): # for now, just pick one at random
  req = wordsUrl+'/phrase'
  rv = requests.get(req)
  return json.loads(rv)

# doesnt do sql COMMIT!!
def word2db(word, pos="NN", ts=-1, src="ip"):
  if ts < 0:  ts = time.time()
  print (word,pos,ts,src)
  try:
    sql =  "insert into word (w, pos, ts, src) values ('{}', '{}', {},'{}'); "\
          .format(word,pos, ts, src)
    #print(sql)
    sql_c.execute(sql)
  except sqlite3.IntegrityError:  # constraint w, pos unique violated: UPDATE count and ts instead of INSERTing
    sql = "update word SET cnt = cnt+1, ts={} where w = '{}' and pos = '{}';".format(ts, word, pos)
    print("DUPLICATE: "+ word + ' ' + pos)
    sql_c.execute(sql)

# doesnt do sql COMMIT!!  tw = array of word,pos pairs as textblob .tags
def phrase2PhraseDB(phraseText, tw, ts=-1, src="ip"):
  if ts < 0:  ts = time.time()
  phraseText.replace("'", "''")
  tw_str = json.dumps(tw)
  sql =  "insert into phrase (ph, tw, ts, src) values ('{}', '{}', {},'{}'); "\
          .format(phraseText,tw_str, ts, src)
  try:
    # print(sql)
    sql_c.execute(sql)
  except:
    print("ERROR ", sql)
    # sqlite3.IntegrityError:  # constraint ph, source unique violated: UPDATE count and ts instead of INSERTing
    # sql = "update word SET ts={} where ph= '{}' and src = '{}';".format(ts, phaseText, tw)
    # print("DUPLICATE: "+ sql)
    # sql_c.execute(sql)

# just a plain text phrase. compute postags and stuff into phrase table.
def text2PhraseDB(text, src="??"):
  text_tb = TextBlob(text)
  ts = time.time()
  phrase2PhraseDB(text, text_tb.tags, ts, src)

def synonyms(theWord, thePOS='NN'):
  rv = []
  poscode = thePOS[0].lower()
  if poscode in ['a','n', 'v']:
    symsets = Word(theWord).lemmatize().get_synsets(pos=poscode)
    for ss in symsets:
      rv.extend(ss.lemma_names())
    print "synonyms of {} {}".format(theWord, rv)
  return rv

# load the words of a whole phrase or text into word table of open words.db
def text2WordDB(theText, ts=-1, src="ip", withSynonyms=False):

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

# ingest a text file into open words.db. not suitable for json files.
def file2WordDB(fname, src):
  with open(fname) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       if len(line) > 5:
         try:
          text2WordDB(line.strip(), -1, src)
          if cnt % 50 == 0:
            print(" {}".format(cnt))
         except:
          print("error reading line ", cnt)
       line = fp.readline()
       cnt += 1

# ingest a text file, w one phrase per line, into open words.db phrase table. not suitable for json files.
def file2PhraseDB(fname, src):
  with open(fname) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
    try:
      text2PhraseDB(line.strip(), src)
      if cnt % 50 == 0:
        print(" {}".format(cnt))
    except:
      print("error reading line ", cnt)
    line = fp.readline()
    cnt += 1
  sql_conn.commit()

# conf  0-9 (minimum confidence), timestamp = minimum timestamp [DEPRECATED]
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

 
def datamuse(word, refcode='rel_trg'):
  # refcode might be
  # ml = "meaning like", 
  # rel_syn = synonym, 
  # rel_trg = trigger, word appearing often near target word in texts
  # rel_jjb = return an adjective
  # rel_ant = antonym
  # for full list see https://www.datamuse.com/api/
  url = "{}?{}={}&md=p".format(datamuseUrl,refcode, word)
  print("datamuse request: url: "+url)
  r = requests.get(url)
  rj = r.json()
  # convert returned data to format used in phrase table: each entry is [<word>,<postag>]
  # verb form is unknow, just give 'V'.. 'XX' for unknown
  trans = {'n': 'NN', 'v': 'V', 'adj': 'JJ', 'adv': 'RB', 'u': 'XX'}
  rv = []
  for x in rj:
    xout = []
    xout.append(x['word'])
    xout.append(trans[x['tags'][0]])
    rv.append(xout)
  return rv 
  
# for convenience, some schlub commands: 
# low-level cmd to say a phrase using schlub server 
def schlubSay(phraseIn, langIn= default_voice,urls=[schlubUrls[0]]):
  theData = json.dumps({"cmd": "Phrase", "args": { "phrase": phraseIn, "reps": 1, "lang": langIn}})
  for u in urls:
    r = requests.post(schlubUrl, data=theData)
    print r

# show a sentence on screen
def schlubShow(phraseIn, urls=[schlubUrls[0]]):
  theData = json.dumps({"cmd": "Show", "args": { "phrase": phraseIn}})
  for u in urls:
   r = requests.post(u, data=theData)

def schlubSoundVol(volIn, urls=[schlubUrls[0]]):
  theData = json.dumps({"cmd": "SoundVol", "args": [volIn]})
  for u in urls:
    r = requests.post(schlubUrl, data=theData)
    print r

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

init()


