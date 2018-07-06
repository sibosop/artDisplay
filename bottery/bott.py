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



if __name__ == '__main__':
# pname = sys.argv[0]
# syslog.syslog(pname+" started at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
# last_timestamp = 0 
# init()

  voices = ['en', 'en-uk', 'en-au']

  dio.schlubSoundVol(30)
  cont = True
  while cont:
    #k = wait_key()
    thePhrase = dio.getPhrase()
    nwords = dio.getNewWords()
    dmu_word =  (random.choice(nwords))[0]
    rwords = dio.datamuse(dmu_word)
    allwords = dio.listMerge(nwords, rwords)
    x  = dio.munge(thePhrase,allwords, 0.4)
    out = dio.wjoin(x)
    theVoice = random.choice(voices)
    print(theVoice, thePhrase[0], out)
    dio.schlubSay(out, theVoice)
    delay = random.randint(7,8)
    print("delay {}".format(delay))
    time.sleep(delay)
    # if k == 'q':
    #   cont = False


