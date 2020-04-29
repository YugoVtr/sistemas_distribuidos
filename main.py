#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from break_hash import hasher
from multiprocessing import Process, Queue

def run_breaker(hash_text, f_hash, wordlist, stack):
    password = hasher(hash_text, f_hash, wordlist)
    stack.put(password)

def build_sub_wordlist( wordlist, size ):
    sub_wordlist = []
    try:
        for i in range(size):
            sub_wordlist.append( next(wordlist) )
        return sub_wordlist
    except:
        pass
    finally:
        return sub_wordlist

if __name__ == "__main__":
    f_hash = hashlib.sha1
    hash_text = f_hash(b"familiapuchis").hexdigest()
    wordlist = open("files/rockyou.txt", 'rb')
    stack = Queue()
    
    sub_wordlist_size = 1793049
 
    sub_wordlist = build_sub_wordlist(wordlist, sub_wordlist_size)
    while len(sub_wordlist) > 0 :        
        p = Process(target=run_breaker, args=(hash_text, f_hash, sub_wordlist, stack,))
        p.start()
        sub_wordlist = build_sub_wordlist(wordlist, sub_wordlist_size)
        
    while not stack.empty():
        password = stack.get()
        if password:
            print("Password is '%s'" % password.decode('utf-8'))
        
    wordlist.close()






