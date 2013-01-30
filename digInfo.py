#!/usr/bin/python
# -*- coding: utf-8 -*-
import BeautifulSoup
import urllib2
import time

infos = [
        u'索书号',
        u'条形码',
        u'登录号',
        u'馆藏地点',
        u'管藏状态',
        u'借出日期',
        u'还回日期',
        u'流通类型',
        u'预约处理',
        u'卷册说明']

infoInsertScript = """insert into bookInfo (
        call_name,
        bar_code,
        login_num,
        store_loca,
        lend_date,
        return_date,
        tran_type,
        order_handle,
        volumn_info,
        commit_time,
        alt_time) values( ?,?,?,?,?,?,?,?,?,?,? )"""


LEN = len( infos )
page = urllib2.urlopen( 'http://opac.its.csu.edu.cn/NTRdrBookRetrInfo.aspx?BookRecno=188' )

soup = BeautifulSoup.BeautifulSoup( page )
print 'done'
print time.time()

def digInfo( soup ):
    bookInfo = {}
    tbody = soup.fetch( 'tbody' )
    if len( tbody ) > 1:
        print 'alert: no only a table'
        return
    trs = tbody[0].fetch('tr')
    for tr in trs:
        tds = tr.fetch('td')
        for i in range( LEN ):
            bookInfo[ infos[i] ] = tds[i].next
    return bookInfo

def main():
    _info = digInfo( soup )
    for i in _info:
        print i,_info[i]
    print time.time()

if __name__ == '__main__':
    main()
