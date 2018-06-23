from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import json
import dataio as dio

PORT = 8081

class GetHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):

      parse = urlparse.urlparse(self.path)
      body = ""
      if (parse.path == "/words" ) :
        pqs = urlparse.parse_qs(parse.query)
        print('pqs', pqs)
        if 'n' in pqs:
            nnew = pqs['n'][0]
        else:
          nnew = 10
        if 'r' in pqs:
          nrand = pqs['r'][0]
        else:
          nrand = 10
        if 'pos' in pqs:
          pos = pqs['pos'][0]
        else:
          pos = ''
        try:
          if(pos == ''):
            body = dio.getWordsDb(nnew,nrand)
            self.send_response(200)
          else:
            body = dio.getWordsDb(nnew,nrand,pos)
            self.send_response(200)
        except:
          body = {"status": "error", "query_str": pqs}
          self.send_response(400)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body))
        return

      if (parse.path == "/phrase") :
        try:
          body = dio.getPhraseDb()
       except:
          body = {"status":"error", "path": parse.path}
          self.send_response(400)
        
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body))

      else:
        body = {"status": "error", "path": parse.path}
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body))
        return
       

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', PORT), GetHandler)
    print 'Starting server on port {}, use <Ctrl-C> to stop'.format(PORT)
    server.serve_forever()
