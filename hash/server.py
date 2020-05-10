#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from main import build_sub_wordlist
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)

class BreakHash(Resource):
    hash_text = hashlib.sha1(b"123kissmybutt").hexdigest()
    wordlist = open("files/rockyou.txt", 'rb')
    sub_wordlist_size = 1793049
    clients = []
    
    def get(self):
        wordlist = build_sub_wordlist(self.wordlist, self.sub_wordlist_size)
        return {
            'hash': self.hash_text, 
            'wordlist': wordlist
        }

    def post(self):
        pwd = request.form['password'] or '0'
        if pwd != '0':
            hextdigest = hashlib.sha1(pwd.encode('utf-8')).hexdigest()
            if self.hash_text == hextdigest:
                msg = "\n\n>>> Senha encontrada no IP %s: '%s' <<<\n\n" % (request.remote_addr, pwd) 
                app.logger.info(msg)
        else:
            msg = "\n\n!!! Senha não encontrada no IP %s !!!\n\n" % (request.remote_addr)
            app.logger.info(msg)

if __name__ == '__main__':
    api = Api(app)
    api.add_resource(BreakHash, '/')
    app.run(debug=True, host='0.0.0.0', port=8080)