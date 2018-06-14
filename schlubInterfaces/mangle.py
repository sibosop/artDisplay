#!/usr/bin/env python
import sys
import json
import random

from textblob import TextBlob

srt_f = open("../lists/pos_all_srt.json","r")
srt_json = srt_f.read()
srt_obj = json.loads(srt_json)

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

   return ' '.join(rv)

if __name__ == '__main__':
  print mangle(sys.argv[1])
