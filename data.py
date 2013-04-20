#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
key argument config
and query script
"""
database = "library.db"
total = 580215.0      #total books
chunk = 10000         # number of books per page
pages = int( round( total / chunk ) )         # total pages
is_fix_fail = False

table_script = """
create table if not exists books (
    id integer primary key,
    bookname    text,
    author      text,
    price       text,
    publisher   text,
    callnum     text,
    isbn        text,
    sortnum     text,
    pages       integer,
    pubdate     text,
    recno       integer,
    which_page  integer,
    commit_time text
);
"""

info_entries = [ u'书名',
    u'作者'
    ,u'价格'
    ,u'出版社'
    ,u'索书号'
    ,u'ISBN'
    ,u'分类号'
    ,u'页数'
    ,u'出版时间'
    ,u'RECNO'
    ,u'which_page']

info_script = u"""insert into books (
    bookname
    ,author
    ,price
    ,publisher
    ,callnum
    ,isbn
    ,sortnum
    ,pages
    ,pubdate
    ,recno
    ,which_page
    ,commit_time) values ( ?,?,?,?,?,?,?,?,?,?,?,datetime('now') )"""

#=====================================================================

# ascending order
# descending order
# descending is default by library site
__ORDER__ = 0
urlbase = 'http://opac.its.csu.edu.cn/NTRdrBookRetr.aspx?strType=text&strKeyValue=*&strpageNum=%s&strSort=%s&page=' % ( chunk,[ 'desc','asc' ][__ORDER__] )
