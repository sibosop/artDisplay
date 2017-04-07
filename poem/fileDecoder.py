#!/usr/bin/env python
from chardet.universaldetector import UniversalDetector
import syslog
import sys
import unicodedata
import codecs
import warnings



class fileDecoder:
  utf8 = {
    'RIGHT SINGLE QUOTATION MARK' : "'"
    ,'EM DASH' : " - "
    ,'LEFT DOUBLE QUOTATION MARK' : "\""
    ,'RIGHT DOUBLE QUOTATION MARK' : "\""
    ,'LATIN SMALL LETTER E WITH DIAERESIS' : "e"
    ,'LATIN SMALL LETTER E WITH GRAVE' : "e"
    ,'LATIN CAPITAL LETTER E WITH DIAERESIS' : "E"
  }
  def __init__(self,textFile):
    warnings.filterwarnings("ignore")
    detector = UniversalDetector()
    for line in file(textFile,'rb'):
      detector.feed(line)
      if detector.done: break
    detector.close()
    syslog.syslog("file is "+str(detector.result))
    self.encoding = detector.result['encoding']
    self.file = codecs.open(textFile,'r',self.encoding)

  def translate(self,c):
    name = unicodedata.name(c)
    try:
      rval = self.utf8[name]
    except KeyError as e:
      rval = ""
      syslog.syslog("translate" +" name:" + name)
    return rval

  def next(self):
    line = self.file.readline()
    if line == "":
      return None
    line = line.strip()
    if self.encoding != 'ascii':
      n = ""
      for c in line:
        try:
          n += c.decode(self.encoding)
        except UnicodeEncodeError as e:
          n += self.translate(c)
      line = n
    return line


if __name__ == '__main__':
  fd = fileDecoder(sys.argv[1])
  while True:
    line = fd.next()
    if line is None: 
      break
    print line
  
