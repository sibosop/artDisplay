#!/usr/bin/env python
import threading
import queue
import time
import syslog
import os
import io

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class recogThread(threading.Thread):
  def __init__(self,i):
    super(recogThread,self).__init__()
    self.name = "Recog Thread"
    self.queue = queue.Queue()
    self.source = i

  def run(self):
    syslog.syslog("starting: "+self.name)
    self.client = speech.SpeechClient()
    self.config = types.RecognitionConfig(
          encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
          sample_rate_hertz=44100,
          language_code='en-US')
    while True:
      content = self.source.get()
      syslog.syslog(self.name+" got "+ str(len(content)))
      audio = types.RecognitionAudio(content=content)
      response = self.client.recognize(self.config,audio)
      syslog.syslog("response num results:"+str(len(response.results)))
      for result in response.results:
        alternatives = result.alternatives
        for alternative in alternatives:
            syslog.syslog('Transcript: {}'.format(alternative.transcript))
            self.queue.put(alternative.transcript)

  def get(self):
    return self.queue.get()

  
