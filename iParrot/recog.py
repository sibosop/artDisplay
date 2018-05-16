#!/usr/bin/env python
import threading
import queue
import time
import syslog
import os
import io
import grpc

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

debug=False

class recogThread(threading.Thread):
  def __init__(self,i):
    super(recogThread,self).__init__()
    self.name = "Recog Thread"
    self.queue = queue.Queue()
    self.source = i
    self.interim = False

  class dataStream(object):
    def __init__(self,r):
      self.recog = r
      if debug: syslog.syslog(self.recog.name+" in dataStream init")
    def __iter__(self):
      if debug: syslog.syslog(self.recog.name+" in dataStream iter")
      return self
    def next(self):
      if debug: syslog.syslog(self.recog.name+" in dataStream next")
      chunk = self.recog.source.get()
      if debug: syslog.syslog(self.recog.name+" got:" + str(len(chunk)))
      return chunk

  def run(self):
    syslog.syslog("starting: "+self.name)
    self.client = speech.SpeechClient()
    while True:
      stream = self.dataStream(self)
      #syslog.syslog(self.name+"for chunk in stream")
      #for chunk in stream:
      #  syslog.syslog(self.name+" chunk size:"+str(len(chunk)))
      requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                  for chunk in stream)
      config = types.RecognitionConfig(
          encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16
          ,sample_rate_hertz=44100
          ,language_code='en-US'
          )
      streaming_config = types.StreamingRecognitionConfig(
                config=config
                ,interim_results=self.interim
                )

      # streaming_recognize returns a generator.
      try:
        responses = self.client.streaming_recognize(streaming_config, requests)
        for response in responses:
          # Once the transcription has settled, the first result will contain the
          # is_final result. The other results will be for subsequent portions of
          # the audio.
          for result in response.results:
              if debug: syslog.syslog('Finished: {}'.format(result.is_final))
              if debug: syslog.syslog('Stability: {}'.format(result.stability))
              alternatives = result.alternatives
              # The alternatives are ordered from most likely to least.
              for alternative in alternatives:
                syslog.syslog('Confidence: {}'.format(alternative.confidence))
                syslog.syslog('Transcript: {}'.format(alternative.transcript))
                out={}
                out['trans'] = alternative.transcript
                out['interim'] = self.interim
                out['confidence'] = alternative.confidence
                self.queue.put(out)

      except grpc.RpcError, e:
        if e.code() not in (grpc.StatusCode.INVALID_ARGUMENT,
                              grpc.StatusCode.OUT_OF_RANGE):
          raise
        details = e.details()
        if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
          #if 'deadline too short' not in details:
          #  raise
          #else:
          #  if 'maximum allowed stream duration' not in details:
          #      raise

          syslog.syslog(self.name +": "+ details + ' Resuming..')



  def get(self):
    return self.queue.get()

  
