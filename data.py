#!/usr/bin/python
# -*- coding: utf-8 -*-
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
