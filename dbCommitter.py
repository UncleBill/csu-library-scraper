#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import libary
import re

insertScript = """insert into books ( author, price, publisher,callnum,isbn, sortnum, pages, pubdate ) values ( "%s","%s","%s","%s","%s","%s","%s","%s" )"""

keyslit = [ '作者','价格','出版者','索书号','ISBN','分类号','出版日期' ]

def dbCommitter( connect,book ):   # book is data
    kl = keyslit
    conn = connect

    author      =    book[kl[0]]
    price       =    book[kl[1]]
    publisher   =    book[kl[2]]
    callnum     =    book[kl[3]]
    isbn        =    book[kl[4]]
    sortnum     =    book[kl[5]]
    p = re.findall('\d+', book[kl[6]] )
    pages = ['None pages',int(p[0])][len(p)>0]
    pubdate     =    book[kl[7]]

    keystuple = tuple( book[i] for i in keyslit )

    conn.execute( insertScript % ( keystuple ) )
    conn.commit()
