#!/usr/bin/python
# -*- coding: utf-8 -*-
""" API for CSU library
    database file:  lib.db
"""

import urllib2
import BeautifulSoup as BS
import sqlite3
import time

from threading import Thread
from Queue import Queue
from time import sleep

from digInfoClass import digInfos

begSec = time.time()
lastTime = begSec
infoInsertScript = digInfos.infoInsertScript
entries = digInfos.entries

BASE = 'http://opac.its.csu.edu.cn/NTRdrBookRetrInfo.aspx?BookRecno='
CHUNK = 100     # commit every $CHUNK books
step = 10000     # handle $step books
libConn = sqlite3.connect('lib.db')
jobQueue = Queue()
ThreadNum = 10
totalFaileds = 0
totalCommit = 0
booklist = []


print 'ThreadNum:', ThreadNum
print begSec

gt = time.gmtime()
urlopener = urllib2.urlopen


def curl(num):
    attempts = 0
    page = False
    url = BASE + str(num)
    while attempts < 10:
        try:
            #page = urlopener( url,timeout=20 )
            page = urlopener(url)
            break
        except:
            attempts += 1
    print attempts,
    return {'page': page, 'num':num}

def nobook( num, errstr=None ):
    print '!e',num,errstr

insertScript = u"""insert into books (
    bookname,
    author,
    price,
    publisher,
    callnum,
    isbn,
    sortnum,
    pages,
    pubdate,
    reno ) values ( ?,?,?,?,?,?,?,?,?,? )"""

keyslit = [ u'书名',u'作者',u'价格',u'出版者',u'索书号',u'ISBN',u'分类号',u'页数',u'出版日期',u'RENO' ]

def pageParser( pg ):
    global booklist
    global totalFaileds
    page, num = pg['page'], pg['num']
    book = {}
    if not page:
        totalFaileds += 1
        return
    try:
        soup = BS.BeautifulSoup( page )
        info = soup.findAll( 'div','info' )   # get name of book
    except TypeError:
        print ''
        return
    infos_list = digInfos( soup ).infos
    if len( info ) < 2:                 # book doesn't exist
        nobook( num, 'There is not this book.Set to None' )
        kl = keyslit
        for k in kl:
            book[k] = u''
        book[u'书名'] = u'No existing!'
        book[u'RENO'] = num
        booklist.append( book )
        return

    book[u'书名'] = info[1].h1.a.text

    lst = soup.fetch('ul','list')       # get details of book
    lst = lst[0]
    details = lst.findAll('li')

    for item in details:
        t = item.span.next
        name =  str( t ).decode('utf-8')
        t = t.next
        if name == u'作者':t = t.next
        value = str( t )
        book[name] = value.decode('utf-8')
    book[u'RENO'] = num
    for infos in infos_list:
        infos[u'RECNO']=num

    book[u'info'] = infos_list
    print '#',
    booklist.append( book )

def dbCommitter( connect,booklist ):   # book is data
    conn = connect
    kl = keyslit

    for item in booklist:
        keys_tuple = tuple(  item[i] for i in kl )
        conn.execute( insertScript ,keys_tuple )
        _infos_list = item[u'info']
        for _i in _infos_list:
            print _i[u'RECNO']
            info_value_tuple = tuple( _i[i] for i in entries )
            conn.execute( infoInsertScript,info_value_tuple )
    conn.commit()

def committer():
    global libConn
    global booklist
    global totalFaileds
    global totalCommit
    global lastTime

    totalCommit += len( booklist )
    if len( booklist ) == 0:
        return
    dbCommitter( libConn, booklist )
    l = len( booklist )
    print '>>>commit!(',l,'books )'
    booklist = []
    print time.ctime()
    print 'total commit',totalCommit
    print 'total failed',totalFaileds
    print 'since last time', time.time() - lastTime
    lastTime = time.time()

def worker():
    while True:
        #pg = curl( jobQueue.get() )
        pg = jobQueue.get()
        pageParser( pg )
        jobQueue.task_done()

for i in range( ThreadNum ):
    th = Thread( target = worker )
    th.setDaemon( True )
    th.start()

def getMax( dbcon, rec = 'reno'):
    max = dbcon.execute( 'select max(reno) from books' ).fetchone()[0]
    if not max:
        max = 0
    return max

def getLowest(lst):
    if len( lst ) == 0:
        return 0
    for i in range( len(lst)-1 ):
        if lst[i+1] - lst[i] > 1:
            print 'lowest:',lst[i]
            return lst[i]
    print 'all ok.lowest:',lst[-1]
    return lst[-1]

def getFail():              # get failed items, ignore $ignore
    global libConn
    # fetch reno column
    renoInDb = libConn.execute( 'select reno from books order by reno' ).fetchall()
    renoList = [ i[0] for i in renoInDb ]
    #badList = range(15000)              # ignore $badList
    #renoList = list( set(renoList) | set(badList) )
    ignore = getLowest( renoList )             # recno less then $ignore is ok
    max = getMax( libConn )
    print 'max:',max
    checkRegion = range( ignore,max,1 )
    failList = list( set(checkRegion) - set(renoList) )
    print 'failed list is built, contains failed:',len( failList )
    return failList

rs = getMax( libConn ) + 1
region = getFail()
region.sort()
region.extend( range( rs,rs + step,1 ) )
print 'will fetch and process ', len( region ), 'pages'

for i in range( len( region ) ):
    pg = curl( region[i] )
    jobQueue.put( pg )
    if i % CHUNK == 0:
        committer()

jobQueue.join()
#libConn.close()
committer()
print time.time() - begSec
