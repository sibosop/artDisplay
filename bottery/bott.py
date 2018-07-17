#!/usr/bin/python

import sys
import os
import random
import time
import argparse

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

# pick words at random from array, weighting longer
def randLonger(arr):
    x = list()
    for w in arr:
        n = len(w)
        for i in range(n):
            x.append(w)
    # print arr, x
    return random.choice(x)

# =================================================================
#        BOT optionsal commands
# =================================================================


def zero():
  cont = True
  while cont:
    if random.choice([0,1]) == 1:

        thePhrase = dio.getPhrase()
        nwords = dio.getNewWords()
        dmu_word =  (random.choice(nwords))[0]
        rwords = dio.datamuse(dmu_word)
    #    print len(rwords)
        allwords = dio.listMerge(nwords, rwords)
        x  = dio.munge(thePhrase,allwords, 0.6)
        out = dio.wjoin(x)
        theVoice = random.choice(voices)
        print("\n{};{}\n{}\n{}".format(theVoice, dio.myName, thePhrase[0], out ))
        dio.schlubSay(out, theVoice, dio.myName)

    else:
        ccwords = dio.getCornCob(3)
        theVoice = random.choice(voices)
        print "******* ", ccwords
        out = dio.wjoin(ccwords)
        dio.schlubSay(out,theVoice, dio.myName)
        dio.schlubShow(out, dio.schlubShowers)

    delay = random.randint(7,8)
#    print("delay {}".format(delay))
    time.sleep(delay)

def foo():
    print "foo! foo! foo!"

def longestWord(wordList):
    #   return the longest word in the list
    rv = ''
    for word in wordList:
        if len(word) > len(rv):
            rv = word
    return(rv)

def randIPWord():
    cont = True
    while cont:
        # get a list of n new ip words and find the longest one
        newWords =  dio.getNewWords(10)
        newWordsOnly = list(map((lambda x: x[0]), newWords))
        randIPWord = randLonger(newWordsOnly)
        print('randIPWord', randIPWord, newWordsOnly)
        dmw = dio.datamuse(randIPWord)
        dmwo = list(map((lambda x: x[0]), dmw))
        thePhrase = dio.getPhrase()
        x = dio.munge(thePhrase,dmw, 0.7)
        out = dio.wjoin(x)
        theVoice = random.choice(voices)
        print "\n{}::{}\n{}\n{}".format(randIPWord, dmwo, thePhrase[0], out)
        dio.schlubSay(out, theVoice, dio.schlubSayers)
        dio.schlubShow(out, dio.schlubShowers)
        delay = random.randint(7,9)
        time.sleep(delay)


def rawMuse():
    # latest ipword in raw datamuse words out.
    cont = True
    while cont:
        # get a list of n new ip words and find the longest one
        newWords =  dio.getNewWords(10)
        theWord = newWords[random.randint(0,9)][0]
        print theWord
        dmw = dio.datamuse(theWord)
        dmwo = list(map((lambda x: x[0]), dmw))
        x = list()
        if len(dmwo) > 0:
            for i in range(5):
                x.append(random.choice(dmwo))
        out = dio.wjoin(x)
        theVoice = random.choice(voices)
        print "\n{}::{}\n{}".format(theWord, dmwo,  out)
        #  theSayers = [random.choice(dio.schlubSayers)]
        # theSayers.append(random.choice(dio.schlubSayers))
        dio.schlubSay(out, theVoice, random.choice(dio.schlubSayers))
        dio.schlubShow(out, dio.schlubShowers)
        delay = random.randint(7,9)
        time.sleep(delay)


def picasso():
    cont = True
    while cont:
        # get a list of n new ip words and find the longest one
        dmw = dio.datamuse('picasso')
        dm_wordsonly = list(map((lambda x: x[0]), dmw))
        thePhrase = dio.getPhrase()
        x = dio.munge(thePhrase,dmw, 0.7)
        out = dio.wjoin(x)
        theVoice = random.choice(voices)
        print "\n{}\n{}\n{}".format(dm_wordsonly, thePhrase[0], out)
        dio.schlubSay(out, theVoice, random.choice(dio.schlubSayers))
        dio.schlubShow(out, dio.schlubShowers)
        delay = random.randint(7,9)
        time.sleep(delay)


def trans():
    cont = True
    while cont:
        theTrans = random.choice(dio.getTrans(3))['trans']
        theVoice = random.choice(voices)
        print "\n{}".format(theTrans)
        dio.schlubSay(theTrans, theVoice, random.choice(dio.schlubSayers))
        dio.schlubShow(theTrans, dio.schlubShowers)
        delay = random.randint(0,8)
        time.sleep(delay)



if __name__ == '__main__':
# pname = sys.argv[0]
# syslog.syslog(pname+" started at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
# last_timestamp = 0 
# init()


  cmd = { 'zero'      : zero
         , 'foo'      : foo 
         , 'picasso'  : picasso
         , 'randword' : randIPWord
         , 'rawmuse'  : rawMuse
         , 'trans'    : trans
        }


  parser = argparse.ArgumentParser()
  parser.add_argument('cmd')
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  args = parser.parse_args()
  debug = args.debug
  print "args = ", args # , args['debug'], args['cmd']
  print args.debug, args.cmd

  voices = ['en', 'en-uk', 'en-au', 'de']

  # dio.schlubSoundVol(30)

  cmd[args.cmd]()



