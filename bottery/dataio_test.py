#!/usr/bin/env python

import dataio as d

# test these routines:

print("DATAIO tests")

print("NO (default) ARGS")

print("selectNewWords", d.selectNewWords(3))
print("selectNewWords", d.selectNewWords())
print("\n\n\n")


print("selectRandomWords", d.selectRandomWords(4))
print("selectRandomWords", d.selectRandomWords())
print("\n\n\n")

print("selectRandomPhrases", d.selectRandomPhrases(3))
print("selectRandomPhrases", d.selectRandomPhrases())
print("\n\n\n")


# http access routines

print("getNewWords", d.getNewWords())
print("getRandomWords", d.getRandomWords())
print("getRandomPhrases", d.getRandomPhrases())

#ingestion routine
d.ingestWords("imitation is the sincerest form of flattery")
print("getNewWords", d.selectNewWords(20))



