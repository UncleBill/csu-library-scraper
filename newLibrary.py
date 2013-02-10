#!/usr/bin/python
# -*- coding: utf-8 -*-
""" API for CSU library
    database file:  $__DATABASE__
"""
import sqlite3
import time
from time import sleep

from threading import Thread
from Queue import Queue

import data
from getSoup import getSoup2
from book_parser import newParser

__DATABASE__ = 'library.new.db'
__INFO__ = 0
__STORE__ = 1
__PAGES__ = 5992
__CHUNK__ = 100         # 100 books per page
__THREAD_NUM__ = 4
__FIX_FAIL__ = False

class library:
    """library class"""
    def __init__(self, database = __DATABASE__):
        self.database = database
        self.db_con = sqlite3.connect(self.database)
        self.beg_time = time.time()
        self.total = {'commit':0,'fail':0}
        self.booklist = []

        self.info_entries = data.info_entries
        self.info_script = data.info_script

        self.job_quenue = Queue()

    def empty_booklist(self):
        self.booklist = []

    def from_page(self):
        _script = 'select count(*) from books'
        _count = self.db_con.execute( _script ).fetchone()[0]
        _page = _count / __CHUNK__ + 1
        return _page

    def commit(self):
        _bl = self.booklist
        self.total['commit'] += len( _bl )
        if len( _bl ) == 0:
            return
        atte = 0
        print 'c',
        while atte < 3:
            try:
                self.commit2db()
                break
            except:
                print 'sleep .5s',
                sleep(0.5)
                atte += 1
        if atte == 3:
            self.commit2db()
        self.state()

    def commit2db(self):
        _con = self.db_con
        # insert basic info
        for book in self.booklist:
            if not book:
                continue
            keys_tuple = tuple(  book[i] for i in self.info_entries )
            _con.execute( self.info_script ,keys_tuple )

        _con.commit()
        self.empty_booklist()

    def state(self):
        print 'commit:',self.total['commit'],
        #print 'fail:',self.total['fail'],
        spend = time.time() - self.beg_time
        print 'use',spend,'s',
        print time.ctime()[10:-4]

    #def worker(self):
        #while True:
            #_soup = self.job_quenue.get()
            #_bklist = newParser().info_parser(_soup)
            #self.booklist.extend(_bklist)
            #self.commit()

    def start(self):
        p = self.from_page() or 0
        print '-'*10,p,'-'*10

        #for i in range(__THREAD_NUM__):
            #th = Thread( target = self.worker )
            #th.setDaemon(True)
            #th.start()

        for page in range(p,__PAGES__,1):
            soupJar = getSoup2(page).soupJar
            if not soupJar:
                print 'stop',page
                break
            #self.job_quenue.put(soup)
            #if page % __THREAD_NUM__ == 0:
                #self.commit()
            self.booklist = newParser().info_parser(soupJar)
            self.commit()
        #self.commit()

def main():
    beg = time.time()
    print time.ctime()
    # start
    library().start()
    print time.ctime()
    print 'use time:',time.time() - beg

if __name__ == '__main__':
    main()
