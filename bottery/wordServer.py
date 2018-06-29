#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import json
import dataio as dio

import socket
myIP = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
PORT = 8081

print("myIP", myIP, "port", PORT)

dio.init_sql()

class GetHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):

      parse = urlparse.urlparse(self.path)
      body = ""

      if (parse.path == "/nw" ) :
        pqs = urlparse.parse_qs(parse.query)
        print('pqs', pqs)
        if 'n' in pqs:
            n = pqs['n'][0]
        else:
          n = 10
        try:
          body = dio.selectNewWords(n)
          self.send_response(200)
        except:
          body = {"status": "error", "query_str": pqs}
          self.send_response(400)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body))
        return

      if (parse.path == "/rw" ) :
        pqs = urlparse.parse_qs(parse.query)
        print('pqs', pqs)
        if 'n' in pqs:
            n = pqs['n'][0]
        else:
          n = 10
        try:
          body = dio.selectRandomWords(n)
          self.send_response(200)
        except:
          body = {"status": "error", "query_str": pqs}
          self.send_response(400)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body))
        return

      if (parse.path == "/ph" ) :
        pqs = urlparse.parse_qs(parse.query)
        print('pqs', pqs)
        if 'n' in pqs:
            n = pqs['n'][0]
        else:
          n = 1
        try:
          body = dio.selectRandomPhrases(n)
          self.send_response(200)
        except:
          body = {"status": "error", "query_str": pqs}
          self.send_response(400)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body))
        return

      else:
        body = {"status": "error", "path": parse.path}
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body))
        return
       

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer((myIP, PORT), GetHandler)
    print 'Starting server on {}:{}, use <Ctrl-C> to stop'.format(myIP, PORT)
    server.serve_forever()
