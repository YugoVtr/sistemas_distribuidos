#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from break_hash import hasher
from multiprocessing import Process, Queue

def build_sub_wordlist( wordlist, size ):
    sub_wordlist = []
    try:
        for i in range(size):
            pwd = next(wordlist)
            if type(pwd) == bytes :
                pwd = pwd.decode('utf-8')
            sub_wordlist.append( pwd.strip() )
    except:
        pass
    finally:
        return sub_wordlist
    
def run_breaker(hash_text, f_hash, wordlist, stack):
    password = hasher(hash_text, f_hash, wordlist)
    stack.put(password)

def run_task(hash_text, f_hash, wordlist):
    stack = Queue()
    procs = []
    
    sub_wordlist_size = 1793049
 
    sub_wordlist = build_sub_wordlist(wordlist, sub_wordlist_size)
    while len(sub_wordlist) > 0 :        
        p = Process(target=run_breaker, args=(hash_text, f_hash, sub_wordlist, stack,))
        procs.append(p)
        p.start()
        sub_wordlist = build_sub_wordlist(wordlist, sub_wordlist_size)
        
    for p in procs:
        p.join()
        
    while not stack.empty():
        password = stack.get()
        if password:
            return password
    
    return None
        






