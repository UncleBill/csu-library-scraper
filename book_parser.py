#!/usr/bin/python
# -*- coding: utf-8 -*-

import data
import time
import lxml.html as html
import urllib2

class parser():
    """basic parser and info parser"""

    def __init__(self):
        self.info_entries = data.info_entries
        self.store_entries = data.store_entries

    def basic_parser(self, soupJar):
        """parse basic infos"""
        soup = soupJar[0]
        num = soupJar[1]
        info_jar = soup.findAll('div','info')
        info = {}
        if len( info_jar ) < 2: # book doesn't exist
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

    def store_parser(self, soupJar):
        """parse store infos"""
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
            store_list.append( store )
        return store_list

class newParser():
    """new parser for new library"""
    def __init__(self):
        self.info_entries = data.info_entries

    def info_parser(self,soupJar):
        print 'start parse',time.ctime()
        soup = soupJar[0]
        num = soupJar[1]
        booklist = []
        result_list = soup.fetch('ul',{'class':'resultlist'})
        for result in result_list:
            book = {}
            # isbn
            isbn_con = result.fetch(id='Cbox')
            if isbn_con:
                isbn = dict(isbn_con[0].attrs)['value']
            else:
                isbn = '0'
            # recno
            recno_con = result.fetch(id='StrTmpRecno')
            if recno_con:
                recno = dict(recno_con[0].attrs)['value']
            else:
                recno = '0'
            # book name
            name = result.fetch('h3',{'class':'title'})[0].text
            # other
            detail_spans = result.fetch('span')[:-5]  # ignore the final five item
            for span in detail_spans:
                k, v = span.text.split(u'：', 1)
                book[k] = v
            book['ISBN'] = isbn
            book['RECNO'] = recno
            book[u'书名'] = name
            book[u'which_page'] = 0 - num
            booklist.append(book)

        print 'parsing success',time.ctime()
        return booklist

class parser3():
    """
    new parser use lxml
    for performence,use lxml
    """

    def __init__(self):
        self.info_entries = data.info_entries

    def info_parser(self,page_num):
        print 'start parse',time.ctime()
        url = data.urlbase + str( page_num )
        page = urllib2.urlopen( url ).read().decode('utf-8')        # decoding is required
        #page = html.parse( url )
        #print page.docinfo.encoding
        #page = page.getroot()
        page = html.fromstring( page )
        booklist = []
        result_list = page.cssselect('ul.resultlist')
        for result in result_list:
            book = {}
            #isbn
            isbn_con = result.cssselect("#Cbox")
            if isbn_con:
                isbn = isbn_con[0].attrib['value']
            else:
                isbn = '0'
            recno_con = result.cssselect("#StrTmpRecno")
            recno = recno_con[0].attrib['value']
            # book name
            name = result.cssselect('h3.title a')[0].text
            # other
            detail_spans = result.cssselect("span")[:-5]    # ignore the final five item
            for span in detail_spans:
                k = span.text[:-1]
                v = span.getchildren()[0].text
                book[k] = v
            book['ISBN'] = isbn
            book['RECNO'] = recno
            book[u'书名'] = name
            book[u'which_page'] = 0 - page_num
            booklist.append(book)

        print 'parsing success',time.ctime()
        return booklist

bookParser = parser3().info_parser     # interface
