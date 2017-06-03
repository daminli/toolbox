# coding=utf-8
'''
Created on 2013-5-26

@author: lidm1
'''
import threading
lock_list = {}

def acquire(lock_key):
    try:
        lock_list[lock_key].acquire()
    except KeyError:
        lock_list[lock_key]=threading.Lock()
        lock_list[lock_key].acquire()

def release(lock_key):
    try:
        lock_list[lock_key].release()
    except KeyError:
        pass