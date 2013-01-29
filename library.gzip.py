#!/usr/bin/python
# -*- coding: utf-8 -*-
""" API for CSU library
    database file:  lib.db
    logfile:        books-%time%.log
"""

import urllib2
import BeautifulSoup as BS
import sqlite3
import time
import gzip

from threading import Thread
from Queue import Queue
from time import sleep
from StringIO import StringIO

begSec =  time.time()
print begSec

BASE = 'http://opac.its.csu.edu.cn/NTRdrBookRetrInfo.aspx?BookRecno='
CHUNK = 50     # commit every $CHUNK books
step = 100     # handle $step books
libConn = sqlite3.connect('lib.db')
jobQueue = Queue()
ThreadNum = 20
totalFaileds = 0
print 'ThreadNum:',ThreadNum
booklist = []

gt = time.gmtime()
#fn = 'log/books-%s-%s-%s-%s.log'%(gt.tm_mday,gt.tm_hour,gt.tm_min,gt.tm_sec)
#lf = file(fn,'a')
urlopener = urllib2.urlopen

def curl( num ):
    attempts = 0
    page = False
    url  = BASE + str( num )
    request = urllib2.Request( url )
    request.add_header( 'Accept-encoding', 'gzip' )     # request gzip for performence
    while attempts < 6:
        try:
            respone = urlopener( request,timeout=20 )
            if respone.info().get( 'Content-Encoding' ) == 'gzip':
                buf = StringIO( respone.read() )
                f = gzip.GzipFile( fileobj = buf )
                page = f.read()
            break
        except :
            attempts += 1
    return {'page':page,'num':num}

def nobook( num ,errstr=None ):
    #global lf
    #lf.write( "e %s %s : %s"%( num, errstr, time.ctime() ) )
    print '!e',num,errstr

insertScript = u"""insert into books (bookname, author, price, publisher,callnum,isbn, sortnum, pages, pubdate, reno ) values ( ?,?,?,?,?,?,?,?,?,? )"""

keyslit = [ u'书名',u'作者',u'价格',u'出版者',u'索书号',u'ISBN',u'分类号',u'页数',u'出版日期',u'RENO' ]

def pageParser( pg ):
    global booklist
    global totalFaileds
    page, num = pg['page'], pg['num']
    book = {}
    if not page:
        #print'!e fail!',num
        totalFaileds += 1
        return
    try:
        soup = BS.BeautifulSoup( page )
    except TypeError:
        print ''
        return
    info = soup.findAll( 'div','info' )   # get name of book

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

    booklist.append( book )

def dbCommitter( connect,booklist ):   # book is data
    kl = keyslit
    conn = connect

    for book in booklist:
        keystuple = tuple(  book[i] for i in kl )

        conn.execute( insertScript,keystuple )
    conn.commit()

def committer():
    global libConn
    global booklist
    global totalFaileds
    dbCommitter( libConn, booklist )
    l = len( booklist )
    print '>>>>commit!(',l,'books )'
    print time.ctime()
    print 'total failed',totalFaileds
    print '-'*30
    booklist = []

def worker():
    while True:
        pg = jobQueue.get()
        pageParser( pg )
        jobQueue.task_done()

for i in range( ThreadNum ):
    th = Thread( target = worker )
    th.setDaemon( True )
    th.start()

def getMax( dbcon, rec = 'reno'):
    max = dbcon.execute( 'select max(reno) from books' ).fetchone()[0]
    return max

def getLowest(lst):
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

#for num in region:
    #pg = curl( num )
    #jobQueue.put( pg )
    #if num % CHUNK == 0:
        #committer()

for i in range( len( region ) ):
    pg = curl( region[i] )
    jobQueue.put( pg )
    if i % CHUNK == 0:
        committer()

jobQueue.join()
#lf.close()
lib.close()
committer()
print time.time() - begSec
