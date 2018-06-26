#!/usr/bin/python

import sys
import os
import random
import time

import dataio as dio

# import sys, os

default_voice = 'en-au'

def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


def utter(langIn= default_voice):
  thePhrase = dio.getPhraseDb()

  words = dio.getwords(20,'NN', 'NNP', 'NNS', 'JJ')
  print(thePhrase[0], words)

  # # get a phrase from the subtitle file
  # srtlen = len(dio.srt)
  # thePhrase = dio.srt[random.randint(0, srtlen)]
  # print "utter: srt len = {}".format(srtlen)
  # print "srt = {}".format(theSRT)
  # # get a bunch of recent words from the word db
  # dbWords =  dio.getwords(20, 'NN', 'NNP', 'NNS','JJ')
  # print("dbWords: {}".format(dbWords))

  # # substitute some words in the srt phrase
  # rv = []
  # for w in thePhrase['tw']:
  #   if w[1] in ['NN', 'NNP', 'NNS', 'JJ']:
  #     rv.append(dio.dbWords.pop()[0])
  #   else:
  #    rv.append(w[0])
  # # print rv
  # rvs = ' '.join(rv).strip().replace('.','').replace(" ' ","'").replace("_"," ")
  # print(rvs)
  dio.schlubSay(thePhrase[0],default_voice)

if __name__ == '__main__':
# pname = sys.argv[0]
# syslog.syslog(pname+" started at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
# last_timestamp = 0 
# init()

  voices = ['en', 'en-uk', 'en-au', 'fr', 'de']

  dio.schlubSoundVol(30)
  cont = True
  while cont:
    #k = wait_key()
    thePhrase = dio.getPhraseDb()
    theVoice = random.choice(voices)
    print(theVoice, thePhrase[0], thePhrase[3])
    dio.schlubSay(thePhrase[0], theVoice)
    delay = random.randint(5,11)
    print("delay {}".format(delay))
    time.sleep(delay)
    # if k == 'q':
    #   cont = False


