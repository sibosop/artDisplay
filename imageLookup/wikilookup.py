#!/usr/bin/env python
import words
import wikipedia
debug=True
def wikilookup(choices):
  lookup=choices[0]+" "+choices[1]
  if debug: print "lookup:",lookup
  res=wikipedia.random(pages=5)
  for k in res:
    print "search",k
    p = wikipedia.page(k)
    print "title:",p.title
    images=p.images
    for i in images:
      print "image:",i
  return []
  


if __name__ == '__main__':
  w=words.Words()
  choices = w.getWords()
  wc=choices[:]
  images=wikilookup(wc)
  for i in images:
    print i