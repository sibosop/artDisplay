# ingest.py    june 2018  t perkis  for Darmstadt
#
#  cmd-lineable functions for  off-line ingestion of various datasources into sql database.
#

import dataio as dio
import sys

# srt files that have had pos tags added can be read into the phrase table
def posjson2PhraseDB(filename, srctag=""):
  if srctag == '':  srctag = filename
  print dio.stopwords



