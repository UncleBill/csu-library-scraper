#!/usr/bin/python
# -*- coding: utf-8 -*-
import BeautifulSoup
import urllib2

class digInfos:
    """docstring for digInfos """
    entries = [
            u'索书号',
            u'条形码',
            u'登录号',
            u'馆藏地点',
            u'管藏状态',
            u'借出日期',
            u'还回日期',
            u'流通类型',
            u'预约处理',
            u'卷册说明',
            u'RECNO']

    infoInsertScript = """insert into bookInfos (
                call_num,
                bar_code,
                login_num,
                store_loca,
                store_state,
                lend_date,
                return_date,
                tran_type,
                order_handle,
                volumn_info,
                recno) values ( ?,?,?,?,?,?,?,?,?,?,? )"""
    def __init__(self,soup):
        self.LEN = len( self.entries ) - 1
        self.soup = soup
        self.infos = self.digger()
    def digger( self ):
        bookInfos = {}
        bookInfosList = []
        tbody = self.soup.fetch( 'tbody' )
        if len( tbody ) > 1:
            print 'alert: no only a table'
            return
        trs = tbody[0].fetch('tr')
        if len( trs ) == 0:
            for i in range( self.LEN ):
                bookInfos[ self.entries[i] ] = 'Empty Info'
            return bookInfos
        for tr in trs:
            tds = tr.fetch('td')
            for i in range( self.LEN ):
                bookInfos[ self.entries[i] ] = tds[i].next
            bookInfosList.append( bookInfos )
        return bookInfosList

def main():
    page = urllib2.urlopen( 'http://opac.its.csu.edu.cn/NTRdrBookRetrInfo.aspx?BookRecno=188' )
    soup = BeautifulSoup.BeautifulSoup( page )
    infos = digInfos ( soup ).infos
    # test
    for i in infos:
        print i,infos[i]
    print len( infos.keys() )
if __name__ == '__main__':
    main()
