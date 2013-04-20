#!/usr/bin/python
# -*- coding: utf-8 -*-
""" API for CSU library
    database file:  $__DATABASE__
"""
import sqlite3
import time

import data
from book_parser import bookParser

__DATABASE__ = data.database
__CHUNK__ = data.chunk      # number of books per page
__PAGES__ = data.pages      # total pages
__FIX_FAIL__ = data.is_fix_fail

class library:
    """
    library class
    =============
    library( string database ): to initialize.
    from_page( self ):genrate first page to fetch
    """

    def __init__(self, database = __DATABASE__):
        self.database = database
        self.db_con = sqlite3.connect(self.database)
        self.db_con.execute( data.table_script )

        self.beg_time = time.time()
        self.total = {'commit':0,'fail':0}      # record commit/fail
        self.booklist = []                      # list to store book entries

        self.info_entries = data.info_entries
        self.info_script = data.info_script

    def _empty_booklist(self):
        """
        set self.booklist empty to release memory
        """
        self.booklist = []

    def from_page(self):
        """
        genrate the first page to fetch
        """
        _script = 'select count(*) from books'
        _count = self.db_con.execute( _script ).fetchone()[0]
        _page = _count / __CHUNK__ + 1
        return _page

    def commit(self):
        """
        committing queue
        """
        _bl = self.booklist
        self.total['commit'] += len( _bl )
        if len( _bl ) == 0:
            return
        atte = 0
        print 'c',
        while atte < 3:     # try 3 times
            try:
                self.commit2db()
                break
            except:
                print 'sleep .2s',      # pause .2s
                time.sleep(0.2)
                atte += 1
        if atte == 3:
            self.commit2db()
        self.status()

    def commit2db(self):
        """
        commit to database
        """
        _con = self.db_con
        # commit basic info
        for book in self.booklist:
            if not book:
                continue
            keys_tuple = tuple(  book[i] for i in self.info_entries )
            _con.execute( self.info_script ,keys_tuple )

        _con.commit()
        self._empty_booklist()

    def status(self):
        """
        print commit status
        """
        print 'commit:',self.total['commit'],
        spend = time.time() - self.beg_time
        print 'use',spend,'s',
        print time.ctime()[10:-4]

    def start(self):
        """
        begin to craw
        """
        p = self.from_page()
        print '-'*10,p,'-'*10
        print __CHUNK__, 'per page'

        for page in range(p,__PAGES__,1):
            self.booklist = bookParser( page ) # for parser3
            self.commit()

    # / library

def main():
    """
    let's go
    """
    beg = time.time()   #<-- time counting
    print time.ctime()
    library().start()   #<-- start
    print time.ctime()
    print 'use time:',time.time() - beg

if __name__ == '__main__':
    main()
