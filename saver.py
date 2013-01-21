#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import libary
import re


#+-----------------------------------------+
#    id integer primary key,
#    author      text,
#    price       text,
#    publisher   text,
#    callnum     text,          # database
#    isbn        text,          # schema
#    sortnum     text,
#    pages       integer,
#    pubdate     text
#+-----------------------------------------+

conn = sqlite3.connect('libary.db')
insertScript = """insert into books ( author, price, publisher,callnum,isbn, sortnum, pages, pubdate ) values ( "%s","%s","%s","%s","%s","%s","%s","%s" )"""

keyslit = [str("作者"),
        str("价格"),
        str("出版者"),
        str("索书号"),
        str("ISBN"),
        str("分类号"),
        str("页数"),
        str("出版日期")
        ]

def main():
    for book in books:
        kl = keyslit
        print type( book )
        author      =    book[kl[0]]
        price       =    book[kl[1]]
        publisher   =    book[kl[2]]
        callnum     =    book[kl[3]]
        isbn        =    book[kl[4]]
        sortnum     =    book[kl[5]]
        p = re.findall('\d+', book[kl[6]] )
        pages = 'None page'
        if len(p) > 0:
            pages = int(p[0])
        pubdate     =    book[kl[7]]
        print "alll:\n"+author,price,publisher,callnum,isbn,sortnum,pages,pubdate
        print 'end'

        #script =  insertScript % ( author, price, publisher,callnum,isbn, sortnum, pages, pubdate )
        keystuple = tuple( book[i] for i in keyslit )
        conn.execute( insertScript % ( keystuple ) )
        #conn.execute( insertScript % ( tuple( book[i] for i in keyslit ) ) )
        conn.commit()

if __name__ == '__main__':
    books = libary.main()

    main()
