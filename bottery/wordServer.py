#!/usr/bin/env python

from datetime import datetime
from flask import Flask, request,jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
import dataio as dio
import sys
import os
import random
# import pygame

# pygame.mixer.init()
# pygame.mixer.music.load("./80z.wav")
# pygame.mixer.music.play()
# 

import socket
myIP = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
PORT = 8081

app = Flask(__name__)
FlaskJSON(app)

@app.route('/nw')
def get_new_words():
    n = request.args.get('n')
    n = 10 if n is None else int(n)
    posar = request.args.get('pos')
    print n, posar
    if (isinstance(posar,str) or isinstance(posar,unicode)) \
        and len(posar) > 0:
        body = dio.selectNewWords(n, posar)
    else:
        body = dio.selectNewWords(n)
    return json_response(data=body)

@app.route('/rw')
def get_random_words():
    n = request.args.get('n')
    n = 10 if n is None else int(n)
    posar = request.args.get('pos')
    print n, posar
    if (isinstance(posar,str) or isinstance(posar,unicode)) \
        and len(posar) > 0:
        body = dio.selectRandomWords(n, posar)
    else:
        body = dio.selectRandomWords(n)
    return json_response(data=body)

@app.route('/ph')
def get_phrases():
    n = request.args.get('n')
    n = 1 if n is None else int(n)
    src = request.args.get('src')
    print n, src
    if(isinstance(src,str) or isinstance(src,unicode)):
        body = dio.selectRandomPhrases(n,src)
    else:
        body = dio.selectRandomPhrases(n)
    return json_response(data=body)

@app.route('/cc')
def get_corncob():
    n = request.args.get('n')
    n = 2 if n is None else int(n)
    body = []
    for i in range(n):
        x = random.choice(linelist).strip()
        body.append(x)
    print body
    return json_response(data=body)

@app.route('/ggl')
def get_ggl_haircut():
    dio.schlubPlay("../bottery/ggl_haircut.wav")
    body = "playing ggl_haircut.wav"
    return json_response(data=body)


@app.route('/col')
def get_colossus():
    dio.schlubPlay("../bottery/colossus.wav")
    body = "playing colossus.wav"
    return json_response(data=body)


# ========= handle errors giving JSON responses

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(status=404, text=str(e)), 404

@app.errorhandler(500)
def internal_err(e):
    return jsonify(status=500, text=str(e)), 500

@app.errorhandler(410)
def page_gone(e):
    return jsonify(status=410, text=str(e)), 410



if __name__ == '__main__':
    os.chdir(os.path.dirname(sys.argv[0]))
    dio.init_sql()

    # load cc list for ccl database.
    choicefile=open("../lists/corncob_lowercase.txt","r")
    linelist=[]
    for line in choicefile:
        linelist.append(line)


    choice=random.choice(linelist)
    print(choice)

    app.run(myIP, PORT)
