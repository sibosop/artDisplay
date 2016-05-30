#!/usr/bin/env python


from subprocess import CalledProcessError, check_output
import sys

def fehTest(path):
  try:
    output = check_output(["feh", "-U",path])
    returncode = 0
  except CalledProcessError as e:
    #print "feh test fails for",path
    output = e.output
    returncode = e.returncode
  return returncode


if __name__ == '__main__':
  fehTest(sys.argv[1])

