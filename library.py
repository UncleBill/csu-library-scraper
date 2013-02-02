#!/usr/bin/python
# -*- coding: utf-8 -*-
""" API for CSU library
    database file:  library.db
"""
import sqlite3
import time

from getSoup import getSoup
import data

__INFO__ = 0
__STORE__ = 1
__STEP__ = 10
__CHUNK__ = 5

class library:
    """docstring for library"""
    def __init__(self, database = 'library.db'):
        self.database = database
        self.key_rec = 'recno'
        self.db_con = sqlite3.connect(self.database)
        self.region = self.gen_region()
        self.beg_time = time.time()
        self.last_time = self.beg_time
        self.total = {'commit':0,'fail':0}
        self.booklist = [ [], [] ]     # booklist[0] contain basic info, booklist[1] contain store info
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
        print '>>commit!(',l,'books )'
        print time.ctime()
        print 'total commit',self.total['commit']
        print 'total failed',self.total['fail']
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

    def nobook(self,a,b):
        print a,b
    def basic_parser(self, soupJar):
        soup = soupJar[0]
        num = soupJar[1]
        info_jar = soup.findAll('div','info')
        info = {}
        if len( info_jar ) < 2: # book doesn't exist
            #self.nobook( num, 'There is not this book.Set to None' )
            kl = self.info_entries
            for k in kl:
                info[k] = u''
            info[u'书名'] = u'No existing!'
            info[u'RECNO'] = num
            return info

        info[u'书名'] = info_jar[1].h1.a.text
        lst = soup.fetch('ul','list')       # get details of book's info
        lst = lst[0]
        details = lst.findAll('li')
        for item in details:
            t = item.span.next
            name =  str( t ).decode('utf-8')
            t = t.next
            if name == u'作者':t = t.next
            value = str( t )
            info[name] = value.decode('utf-8')
        info[u'RECNO'] = num
        return info

    def storeparser(self, soupJar):
        soup = soupJar[0]
        num = soupJar[1]
        tbody = soup.fetch( 'tbody' )
        store = {}
        store_list = []
        if len( tbody ) > 1 or len(tbody) < 1:
            print '!alert: not just a table'
            return None
        trs = tbody[0].fetch('tr')
        if len( trs ) == 0:     # when no store info.
            for i in range(10):
                store[ self.store_entries[i] ] = 'Empty Info'
            store['RECNO'] = num
            store_list.append( store )
            return store_list
        for tr in trs:          # save in a store info. list
            tds = tr.fetch('td')
            for i in range(10):
                store[ self.store_entries[i] ] = tds[i].next
            store['RECNO'] = num
            store_list.append( store)
        return store_list

    def start(self):
        for i in self.region:
            _soupJar = getSoup(i).soupJar
            if not _soupJar:
                # handle error page
                self.total_fail += 1
                continue
            info = self.basic_parser(_soupJar)
            store = self.storeparser(_soupJar)
            self.booklist[__INFO__].append(info)
            self.booklist[__STORE__].append(store)
            if i % __CHUNK__ == 0:
                self.commit()

def main():
    beg = time.time()
    print time.ctime(),beg
    library().start()
    print time.ctime()
    print 'use time:',time.time() - beg

if __name__ == '__main__':
    main()
