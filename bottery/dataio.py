#!/usr/bin/env python


# dataio.py     perkis june 2018 for Darmstadt
#
#   For Loading into sqlite tables:
#     * dataio.ingestWords()  takes any phrase/short text, postags it and ingests the words in it into the word database (sqlite)
#     * dataio.ingestTaggedWord() is called by above to write individual words to db with pos taggin
#     * dataio.ingestFileWords() will ingest a given text file into the word database w repeated calls to text2WordDB for each line.
#     * dataio.ingestPhrase()
# 
#    For reading sqlite tables through web interface.
#     * dataio.getRandWords() retrieves word lists from the words database word table
#     * dataio.getNewWords()
#     * dataio.getRandomPhrases
#
#    For accessing database through sql:
#     * selectRandWords()
#     * selectNewWords()
#     * selectRandomPhrase()
#
#    For word data generations
#     * dataio.synonyms() uses wordnet to get synotnyms of a given (pos-tagged) word
#     * dataio.datamuse() uses the datamuse.com api to get related words to a given word.
#
#    For schlub server output:
#     * dataio.schlubSay(), 
#     * dataio.schlubShow(), 
#     * dataio.schlubSoundVol()
#
# read in the words.db on startup and on exit persist the words.db to file.


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
import itertools

import socket
myIP = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
print("myIP", myIP)

debug = False

# parrotUrl        = None
# parrotDisplayUrl = None
schlubSayers     = None
schlubShowers    = None
wordsUrl         = None
datamuseUrl      = "http://api.datamuse.com/words"
transUrl         = None

stopwords_filename = "../lists/stopwords.json"
sqlite_filename    = "../lists/words.db"
voices = ['en-au', 'en-uk', 'en', 'de']
default_voice = 'en-au'

config = {} # will be overwritten by read of config/schlub.js in init()

# to be init'ed by init()
sql_conn = ''
sql_c    = ''

# utility convert u'blahblah' strings from unicode to ascii
def nu(s):
  return s.encode('ascii', 'ignore')

def init_sql():
  global sql_conn, sql_c

  sql_conn = sqlite3.connect(sqlite_filename)
  sql_c = sql_conn.cursor()

def db_report():
  print "stopwords length: {}".format(len(stopwords))
  sql_c.execute("select count() from word;")
  print("words in database: {}".format(sql_c.fetchone()[0]))
  sql_c.execute("select count() from phrase;")
  print ("phrases in database: {}".format(sql_c.fetchone()[0]))


def init():
  global stopwords, words, config
  global parrotName, wordsUrl, transUrl
  global myName, schlubSayers, schlubShowers

  # first read schlub.json with ip addresses of all our
  with open("../config/schlub.json") as fp:
    config  = json.load(fp)

  # set myName by lookup from myIP in config.
  # build schlubShowers and schlubSayers lists.
  schlubSayers = list()
  schlubShowers = list()

  for h in config['hosts']:
    if h['ip'] == myIP:
      myName = h['name']
    if h['hasAudio'] == True:
      schlubSayers.append(h['name'])
    if h['hasScreen'] == True:
      schlubShowers.append(h['name'])
    if h['name'] == config['parrotName']:
      wordsUrl = "http://{}:{}".format(h['ip'], config['wordServerPort'])
      transUrl = "http://{}:{}".format(h['ip'], config['transServerPort'])



  parrotName = config['parrotName']
  # wordsUrl = parrotUrl
  # parrotDisplayUrl = "http://{}:{}".format(config['parrotDisplayIp'], config['schlubServerPort'])

  # load up 'database' dict objects from json files
  with open(stopwords_filename) as json_stopwords:   
    stopwords  = json.load(json_stopwords)
  # with open(words_filename) as json_words:           
  #   words      = json.load(json_words)

  #test -- print out wordtank
  # print("words", words)
  # print(stopwords)
  print "====== DATAIO ============"
  print "schlubSayers: ", schlubSayers
  print "schlubShowers: ", schlubShowers
  print "parrotName", parrotName
  print "wordsUrl", wordsUrl
  print "transUrl", transUrl
  print "====== DATAIO ============"


init()
init_sql()


 
# ================================
#  sqlite select query routines
# ================================

def selectNewWords(n=10, pos=''):
  if len(pos) > 0:
    pos = "'"+pos.replace(' ', "','")+"'"
    sql = "select * from word where pos in ({}) ".format(pos)
  else:
    sql = "select * from word "
  sql += "order by ts desc limit {};".format(n)
  if debug:
    print(sql)
  sql_c.execute(sql)
  newWords = list(sql_c.fetchall())
  return(newWords)

def selectRandomWords(n=10, pos=''):
  if len(pos) > 0:
    pos = "'"+pos.replace(' ', "','")+"'"
    sql = "select * from word where pos in ({}) ".format(pos)
  else:
    sql = "select * from word "
  sql += "order by RANDOM() limit {};".format(n)
  if debug:
    print(sql)
  sql_c.execute(sql)
  theWords = list(sql_c.fetchall())
  random.shuffle(theWords)
  return(theWords)

def selectRandomPhrases(n=1, src= "any"): 
  sql = "select * from phrase "
  if src != "any":
    sql += " where src = '{}' ".format(src)
  sql +=" order by RANDOM() LIMIT {};".format(n)
  if debug:
    print(sql)
  sql_c.execute(sql)
  sr = sql_c.fetchall()
  #return sr
  # tw array is stringified in db; restore it to objecthood
  rv =  [[r[0], json.loads(r[1]), r[2], r[3]] for r in sr]
  return(rv)

# ================================================
#  http wordserver client routines
# ================================================

def getNewWords(n=10,  pos=''):
  if len(pos) > 0:
    pos = pos.replace(' ', '+')
    req = wordsUrl+'/nw?n='+str(n)+'&pos='+pos
    #print req
    rv = requests.get(req)
  else:
    req = wordsUrl+'/nw?n='+str(n)
    #print('req', req)
    rv = requests.get(req)
    # print('rv', rv.text)

  return json.loads(rv.text)['data']

def getRandomWords(n=10, pos=''):
  if len(pos) > 0:
    pos = pos.replace(' ', '+')
    req = wordsUrl+'/rw?n='+str(n)+'&pos='+pos
    print req
    rv = requests.get(req)
  else:
    req = wordsUrl+'/rw?n='+str(n)
    print req
    rv = requests.get(req)

  return json.loads(rv.text)['data']

def getRandomPhrases(n = 1, src= ''): # for now, just pick one at random
  req = wordsUrl+'/ph?n='+str(n)
  if len(src) > 0:
   req += '&src='+src
  rv = requests.get(req)
  return json.loads(rv.text)['data']

def getPhrase(): # just one random phrase
  rv = getRandomPhrases(1)
  return rv[0]

def getCornCob(n=2):
  req = wordsUrl+'/cc?n='+str(n)
  rv = requests.get(req)
  return json.loads(rv.text)['transcript']


# =============================================
#   iParrot transcript server routines
# =============================================
def getTrans(ct = 0):
  req = transUrl+'/data?ct='+str(ct)
  rv = requests.get(req)
  return json.loads(rv.text)['transcript']




# =============================================
#   database data ingestion routines
# =============================================

# doesnt do sql COMMIT!!
def ingestTaggedWord(word, pos="NN", ts=-1, src="ip"):
  if ts < 0:  ts = time.time()
  # print (word,pos,ts,src)
  try:
    sql =  "insert into word (w, pos, ts, src) values ('{}', '{}', {},'{}'); "\
          .format(word,pos, ts, src)
    print(sql)
    sql_c.execute(sql)
  except sqlite3.IntegrityError:  # constraint w, pos unique violated: UPDATE count and ts instead of INSERTing
    sql = "update word SET cnt = cnt+1, ts={} where w = '{}' and pos = '{}';".format(ts, word, pos)
    print("DUPLICATE: "+ word + ' ' + pos)
    print sql
    sql_c.execute(sql)
  except Exception, e:
    print e

# doesnt do sql COMMIT!!  tw = array of word,pos pairs as textblob .tags
def ingestTaggedPhrase(phraseText, tw, ts=-1, src="??"):
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

# given just a plain untagged text phrase, compute postags and stuff into phrase table.
def ingestPhrase(text, src="??"):
  text_tb = TextBlob(text)
  ts = time.time()
  ingestTaggedPhrase(text, text_tb.tags, ts, src)

# load the words of a whole phrase or text into word table of open words.db
def ingestWords(theText, ts=-1, src="ip"):

  if ts < 0: ts = time.time()
  
  text_tb = TextBlob(theText)
  #print text_tb

  for w in text_tb.tags:
    if not w[0].lower() in stopwords:
      ingestTaggedWord(w[0].lower(), w[1], ts, src)

  sql_conn.commit()

# ingest a text file into open words.db. not suitable for json files.
def ingestFileWords(fname, src):
  with open(fname) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       if len(line) > 5:
         try:
          ingestWords(line.strip(), -1, src)
          if cnt % 50 == 0:
            print(" {}".format(cnt))
         except:
          print("error reading line ", cnt)
       line = fp.readline()
       cnt += 1

# ingest a text file, w one phrase per line, into open words.db phrase table. not suitable for json files.
def ingestFilePhrases(fname, src):
  with open(fname) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
    try:
      ingestPhrase(line.strip(), src)
      if cnt % 50 == 0:
        print " {}".format(cnt),
        sys.stdout.flush()
    except:
      print("error reading line ", cnt)
    line = fp.readline()
    cnt += 1
  sql_conn.commit()
  print (cnt - 1)


# ===========================================
#   text/words data generation routines
# ===========================================

def synonyms(theWord, thePOS='NN'):
  rv = []
  poscode = thePOS[0].lower()
  if poscode in ['a','n', 'v']:
    symsets = Word(theWord).lemmatize().get_synsets(pos=poscode)
    for ss in symsets:
      rv.extend(ss.lemma_names())
    print "synonyms of {} {}".format(theWord, rv)
  return rv


 
def datamuse(word, refcode='rel_trg'):
  # refcode might be
  # ml = "meaning like", 
  # rel_syn = synonym, 
  # rel_trg = trigger, word appearing often near target word in texts
  # rel_jjb = return an adjective
  # rel_ant = antonym
  # for full list see https://www.datamuse.com/api/
  url = "{}?{}={}&md=pf".format(datamuseUrl,refcode, word)
  # print("datamuse request: url: "+url)
  r = requests.get(url)
  rj = r.json()
  # convert returned data to format used in phrase table, with addition
  # if word frequency:  each entry is [<word>,<postag>, <frequency>]
  # verb form is unknow, just give 'V'.. 'XX' for unknown
  trans = {'n': 'NN', 'v': 'V', 'adj': 'JJ', 'adv': 'RB', 'u': 'XX'}
  rv = []
  for x in rj:
    xout = []
    try:
      xout.append(x['word'])
      xout.append(trans[x['tags'][0]]) #pos
      wftag = x['tags'][1]
  #   print x['word'],wftag
      if 'f:' in wftag:
        xout.append(wftag[2:]) #word frequency
      else:
        xout[1] = 'NNP'
      rv.append(xout)
    except: pass
  return rv 
  
# =====================================
#    schlub output commands
# =====================================
def schlubUrl(name):
  for h in config['hosts']:
    if nu(h['name']) == name:
      return "http://{}:{}".format(h['ip'], config['schlubServerPort'])

  return "ERROR: NO PORT OF NAME " + name + " FOUND"

def schlubSay(phraseIn, langIn= default_voice,sayers=[schlubSayers[0]]):
  if (isinstance(sayers,str) or isinstance(sayers,unicode)):
    sayers = [sayers]
  phraseIn = phraseIn.replace('I ', 'eye ')
  theData = json.dumps({"cmd": "Phrase", "args": { "phrase": phraseIn, "reps": 1, "lang": langIn}})
  for s in sayers:
    u =  schlubUrl(s)
    r = requests.post(u, data=theData)
    #print r.text

# show a sentence on screen
def schlubShow(phraseIn, showers=[schlubShowers[0]]):
  if (isinstance(showers,str) or isinstance(showers,unicode)):
    showers = [showers]
  theData = json.dumps({"cmd": "Show", "args": { "phrase": phraseIn}})
  for s in showers:
   u = schlubUrl(s)
   r = requests.post(u, data=theData)
   # print r.text

def schlubSoundVol(volIn, sayers=[schlubSayers[0]]):
  if (isinstance(sayers,str) or isinstance(sayers,unicode)):
    sayers = [sayers]
  theData = json.dumps({"cmd": "SoundVol", "args": [volIn]})
  for s in sayers:
    u = schlubUrl(s)
    r = requests.post(u, data=theData)
    print r.text


def schlubVol(volIn, sayers=[schlubSayers[0]]):
  if (isinstance(sayers,str) or isinstance(sayers,unicode)):
    sayers = [sayers]
  theData = json.dumps({"cmd": "Volume", "args": [volIn]})
  for s in sayers:
    u = schlubUrl(s)
    r = requests.post(u, data=theData)
    print r.text

# play one sound.. path relative to artDisplay/schlub
def schlubPlay(filepath, sayers=[schlubSayers[0]]):
  theData = json.dumps({"cmd" : "Play", "args": { "path" : filepath}})
  for s in sayers:
    u = schlubUrl(s)
    try:
      r = requests.post(u, data=theData, timeout=2.0)
      print r.text
    except Exception as e:
      print str(e)



# ==============================================================================

def listMerge(*theLists): # each arg should be a word list
  x = list(itertools.chain.from_iterable(theLists))
  return x

# make a dictionary keyed by pos of a postagged word list.
def makePosDict(wordlist):
  rv = {}
  for w in wordlist:
    tag = w[1]
    wd = w[0]
    if tag in rv:
      rv[tag].append(wd)
    else:
      rv[tag] = [wd]

  return rv

# join a list of (untagged) words into a pronouncable phrase.
def wjoin(x):
  rv = ''
  for w in x:
    # print('|'+rv+'| {'+w+'}')
    if w in "!.,;?":
      rv += w
    else:
      rv += ' '+w
  return rv.strip().replace('...','').replace('_', ' ').replace('-', '')

def munge(phrase, wordlist, prob):
  random.shuffle(wordlist)
  posDict = makePosDict(wordlist)
  # print("===============================")
  # print(posDict)
  # print("===============================")
  rv = []
  for w in phrase[1]:
    tag = w[1]
    if tag in posDict \
    and (random.random() < prob) \
    and len(posDict[tag]) > 0 \
    and w[0] != 'I':
#      print " subst", prob,
      rv.append(posDict[tag].pop())
    else:
#      print " orig", prob,
      rv.append(w[0])
  return rv


def munge_test(prob):
  init_sql()
  ph = getPhrase()
  wl = getRandomWords(40)
  x  = munge(ph,wl, prob)
  out = wjoin(x)
  if not (out[-1] in "!.,;?"): out += '.'
  print ph[1]
  print ph[0]
  print out
  schlubShow(out)
  schlubSay(out, random.choice(['en', 'en-uk', 'en-au', 'fr', 'de']))
  #schlubShow(out)

def munge_new(prob):
  init_sql()
  ph = getPhrase()
  wl = getNewWords(40)
  x  = munge(ph,wl, prob)
  out = wjoin(x)
  if not (out[-1] in "!.,;?"): out += '.'
  print ph[1]
  print ph[0]
  print out
  schlubShow(out)
  schlubSay(out, random.choice(['en', 'en-uk', 'en-au', 'de']))
  #schlubShow(out)


# ============================================================================
# def byebye():
#   sql_conn.close()
#   # save updated json words database file.
#   # write a backup of the old file before writing.

#   # global words
#   # copyfile(words_filename, words_filename + '.bu'+str(int(time.time())))
#   # with open(words_filename, 'w') as outfile:  
#   #   json.dump(words, outfile, indent=2)
#   # print('updated wordtank', words)

#   print("dataio sez byebye")



