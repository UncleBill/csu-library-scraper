#!/usr/bin/python
# -*- coding: utf-8 -*-
""" API for CSU library
    database file:  library.db
"""
import sqlite3
import time

from getSoup import getSoup
from book_parser import parser
import data

__INFO__ = 0
__STORE__ = 1
__STEP__ = 20000
__CHUNK__ = 50

class library:
    """library class"""
    def __init__(self, database = 'library.db'):
        self.database = database
        self.key_rec = 'recno'
        self.db_con = sqlite3.connect(self.database)
        self.region = self.gen_region()
        self.beg_time = time.time()
        self.last_time = self.beg_time
        self.total = {'commit':0,'fail':0}
        # booklist[0] contain basic info, booklist[1] contain store info
        self.booklist = [ [], [] ]

        self.info_entries = data.info_entries
        self.info_script = data.info_script
        self.store_entries = data.store_entries
        self.store_script = data.store_script

    def gen_region(self):
        _max = self.get_max_rec( self.db_con ) + 1
        region = self.fail_list()
        region.sort()
        ext = range( _max, _max + __STEP__, 1 )
        region.extend(ext)
        return region

    def get_max_rec(self, rec = 'recno'):
        _script = 'select max(recno) from books'
        _max = self.db_con.execute( _script ).fetchone()[0]
        if not _max:
            _max = 1
        print 'find the max',_max
        return _max

    def get_lowest(self,lst):
        if len( lst ) == 0:
            print 'An empty database'
            return 0
        for i in range( len(lst)-1 ):
            if lst[i+1] - lst[i] > 1:
                print 'lowest:', lst[i]
                return lst[i]
        print 'find the lowest recno',lst[-1]
        return lst[-1]

    def fail_list(self):
        _script = 'select recno from books order by recno'
        recno_in_db = self.db_con.execute( _script ).fetchall()
        recno_list = [ i[0] for i in recno_in_db ]
        if len( recno_list ) == 0:
            return [0]

        ignore = self.get_lowest( recno_list )
        _max = self.get_max_rec()
        check_region = range( ignore, _max, 1 )
        failList = list( set(check_region) - set(recno_list) )
        print 'failed list is built, contains failed:',len( failList )
        return failList

    def commit(self):
        _bl = self.booklist[0]
        self.total['commit'] += len( _bl )
        if len( _bl ) == 0:
            return
        self.commit2db()
        l = len( _bl )
        print '>>commit!(',l,'books )',
        self.state()
        print 'since last time', time.time() - self.last_time,'s'

        self.last_time = time.time()

    def commit2db(self):
        _con = self.db_con
        # insert basic info
        for item in self.booklist[__INFO__]:
            if not item:
                continue
            keys_tuple = tuple(  item[i] for i in self.info_entries )
            _con.execute( self.info_script ,keys_tuple )
        # insert store info
        for line in self.booklist[__STORE__]:
            for item in line:
                if not item:
                    continue
                l = [item[i] for i in self.store_entries]
                store_value_tuple = tuple( l )
                _con.execute( self.store_script, store_value_tuple )

        _con.commit()
        self.booklist = [ [], [] ]      # rempty booklist

    def state(self):
        print time.ctime()
        print 'total commit:',self.total['commit'],
        print 'total failed:',self.total['fail']

    def start(self):
        size = len( self.region )
        print 'will process',size,'books'
        for i in range(size):
            seed = self.region[i]
            _soupJar = getSoup(seed).soupJar
            if not _soupJar:
                # TODO handle error page
                #for i in basic_entires:
                    #info[i] = 'FAIL_PAGE'
                #for i in store_entries:
                    #store[i] = 'FAIL_PAGE'

                #store[u'RECNO'] = info[u'RECNO'] = seed
                #self.booklist[__INFO__].append(info)
                #self.booklist[__STORE__].append([store])

                self.total['fail'] += 1
            else:
                info = parser.basic_parser(_soupJar)
                store = parser.store_parser(_soupJar)
                self.booklist[__INFO__].append(info)
                self.booklist[__STORE__].append(store)
            if i % __CHUNK__ == 0:
                self.commit()
        self.state()

def main():
    beg = time.time()
    print time.ctime(),beg
    library().start()
    print time.ctime()
    print 'use time:',time.time() - beg

if __name__ == '__main__':
    main()
