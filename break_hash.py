#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.decorators import coroutine

def hasher(hexdigest, f_hash, word_list):
    test = test_hash(hexdigest, f_hash)
    for password in word_list:
        pwd = password.strip()
        if test.send( pwd ): 
            return pwd

@coroutine
def test_hash(test_pwd, f_hash):
    try:
        while True:
            password = (yield)
            hashed = f_hash(password).hexdigest()
            if test_pwd == hashed:
                yield password
    except GeneratorExit:
        return None

