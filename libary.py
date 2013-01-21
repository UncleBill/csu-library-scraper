#!/usr/bin/python
# -*- coding: utf-8 -*-
""" API for CSU libary"""

import urllib2
import BeautifulSoup as BS
import pickle
import sqlite3
import re

from dbCommitter import dbCommitter

_base = 'http://opac.its.csu.edu.cn/NTRdrBookRetrInfo.aspx?BookRecno='

libary = sqlite3.connect('libary.db')

def curl(url):
    try:
        page = urllib2.urlopen( url,timeout=20 )
    except:
        return False
    return page

def dump2file(obj,filestr):
    wfile = open( filestr,'wb' )
    pickle.dump( obj, wfile )
    wfile.close()

def main():
    for num in range(406360,406390,1):
        book = {}
        page = curl( _base + str( num ) )
        if not page:
            print num,'err'
            continue
        html = BS.BeautifulSoup( page )

        lst = html.fetch('ul','list')
        if not len(lst): continue
        lst = lst[0]
        details = lst.findAll('li')

        for item in details:
            t = item.span.next
            name = str( t )
            t = t.next
            if str(name) == '作者':t = t.next
            value = str( t )

            book[name] = value
        dbCommitter( libary, book )

if __name__ == '__main__':
    main()
