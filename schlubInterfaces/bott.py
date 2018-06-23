import dataio as dio

def utter(langIn= default_voice):
  # get a srt phrase from the subtitle file
  srtlen = len(dio.srt)
  theSRT = dio.srt[random.randint(0, srtlen)]
  print "utter: srt len = {}".format(srtlen)
  print "srt = {}".format(theSRT)
  # get a bunch of recent words from the word db
  dbWords =  dio.getwords(20, 'NN', 'NNP', 'NNS','JJ')
  print("dbWords: {}".format(dbWords))

  # substitute some words in the srt phrase
  rv = []
  for w in theSRT['tw']:
    if w[1] in ['NN', 'NNP', 'NNS', 'JJ']:
      rv.append(dio.dbWords.pop()[0])
    else:
     rv.append(w[0])
  # print rv
  rvs = ' '.join(rv).strip().replace('.','').replace(" ' ","'").replace("_"," ")
  print(rvs)
  dio.schlubSay(rvs,langIn)

if __name__ == '__main__':
pname = sys.argv[0]
syslog.syslog(pname+" started at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
last_timestamp = 0 
init()

while True:
  transcript = dio.hitParrot(0,last_timestamp)
  if len(transcript) > 0:
   last_timestamp = int(math.ceil(transcript[0]['timestamp']))
   print len(transcript)
   for x in transcript:
     thePhrase = x['trans'].strip()
     if x['confidence'] > 0.7:
       dio.schlubSay(thePhrase, dio.default_voice )
       print(thePhrase)
     dio.schlubShow(thePhrase)
  sys.stdout.write('.')
  sys.stdout.flush()
  time.sleep(2)




