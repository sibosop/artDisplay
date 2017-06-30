#!/usr/bin/env python
import BaseHTTPServer
import threading
import time
import syslog
import schlubTrack

debug=True


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
  def do_GET(s):
    """Respond to a GET request."""
    syslog.syslog("path = "+s.path)
    status = s.server.play(s.path)
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    #s.wfile.write("<html><head><title>Title goes here.</title></head>")
    #s.wfile.write("<body>")
    # If someone went to "http://something.somewhere.net/foo/bar/",
    # then s.path equals "/foo/bar/".
    s.wfile.write(status)
    s.wfile.write("</body></html>")

  def log_message(self, format, *args):
    syslog.syslog("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

class soundServer(BaseHTTPServer.HTTPServer):
  def __init__(self,client,handler):
    BaseHTTPServer.HTTPServer.__init__(self,client,handler)
    self.test = "test var"

  def play(self,args):
    test=args.split("?")
    rval = "fail\n"
    if len(test) != 2:
      if debug: syslog.syslog("soundServer ignoring:",path)
    else:
      cmds=test[1].split("=")
      if cmds[0] != 'play':
        if debug: syslog.syslog("soundServer ignoring: "+args)
      else:
        if len(cmds) < 2:
          if debug: syslog.syslog("soundServer ignoring: "+args)
        else:
          syslog.syslog("doing "+args)
          schlubTrack.setCurrentSound(cmds[1])
          rval = "ok\n"
          
    return rval;


class soundServerThread(threading.Thread):
  def __init__(self,port):
    super(soundServerThread,self).__init__()
    self.port = port
    syslog.syslog("sound server:"+str(self.port))
    #self.server_class = BaseHTTPServer.HTTPServer
    self.server_class = soundServer
    self.httpd = self.server_class(('', self.port), MyHandler)

  def run(self):
    self.httpd.serve_forever()

