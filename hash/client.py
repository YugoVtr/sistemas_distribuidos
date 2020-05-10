#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, hashlib
from main import run_task

if __name__ == '__main__': 
    url = "http://127.0.0.1:8080/"
    response = requests.get(url).json()
    wordlist = iter(response['wordlist'])
    flag = len(response['wordlist']) > 0
 
    while flag:
        password = run_task(response['hash'], hashlib.sha1, wordlist)
        requests.post(url, {'password': (password or 0)})
        
        if not password:
            response = requests.get(url).json()
            wordlist = iter(response['wordlist'])
            flag = len(response['wordlist']) > 0
        else:
            flag = False