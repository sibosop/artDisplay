#!/usr/bin/env python
import roman
import sys

if __name__ == '__main__':
  with open(sys.argv[1]) as f:
    for line in f:
      l = line.strip()
      n = roman.roman_to_int(l)
      if n:
        print "found:",l,n


