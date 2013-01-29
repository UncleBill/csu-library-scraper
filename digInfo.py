#!/usr/bin/python
# -*- coding: utf-8 -*-
import BeautifulSoup

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

bookInfo = {}

LEN = len( infos )

soup = BeautifulSoup.BeautifulSoup( page )

def digInfo( soup ):
    tbody = soup.fetch( 'tbody' )
    if len( tbody ) > 1:
        print 'alert: no only a table',num
        return
    trs = tbody.fetch('tr')
    for i in range( LEN ):
        t = trs[i]
        bookInfo[infos[i]] = t.next.next

def BKInfoCommitter( libCon, infolist ):
    for info in infolist:

        libCon.execute()
