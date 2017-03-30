#!/usr/bin/env python
import re

numeral_map = None

def sonnetRe():
  return re.compile('^[IVXLCDM]+$')


def roman_to_int(n,re=sonnetRe):
  global numeral_map
  if numeral_map is None:
    numeral_map = zip(
      (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
      ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    )
  n = n.strip()
  if re().match(n) is None:
    #print n,": not a match"
    return 0
  i = result = 0
  for integer, numeral in numeral_map:
    while n[i:i + len(numeral)] == numeral:
      result += integer
      i += len(numeral)
  return result
