#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import BeautifulSoup as bs

__TRY__ = 3

class getSoup():
    """docstring for getSoup"""
    def __init__(self, num):
        self.base = 'http://opac.its.csu.edu.cn/NTRdrBookRetrInfo.aspx?BookRecno='
        self.num = num
        self.url = self.base + str(num)
        self.soupJar = self.getSoup()

    def curl(self):
        attempts = 0
        page = False
        while attempts < __TRY__:
            try:
                page = urllib2.urlopen(self.url,timeout=100)
                break
            except:
                attempts += 1
        if attempts == 0:
            print '-',
        elif attempts == __TRY__:
            print '#',
        else:
            print attempts,
        return page

    def getSoup(self):
        page = self.curl()
        if not page:
            return None
        try:
            soup = bs.BeautifulSoup( page )
            return [soup, self.num]
        except:
            print 'type error',self.num
            return None

class getSoup2(getSoup):
    """getSoup for newLibrary"""
    def __init__(self,num):
        self.num = num
        self.base = 'http://opac.its.csu.edu.cn/NTRdrBookRetr.aspx?strType=text&strKeyValue=*&strpageNum=100&strSort=asc&page='
        self.url = self.base + str(num)
        self.soupJar = self.getSoup()

    def curl(self):
        attempts = 0
        page = False
        #page = urllib2.urlopen(self.url,timeout=180)
        while attempts < __TRY__:
            try:
                page = urllib2.urlopen(self.url,timeout=180)
                break
            except:
                attempts += 1
        if attempts == 0:
            print '-',
        elif attempts == __TRY__:
            print '#',
        else:
            print attempts,
        return page

    def getSoup(self):
        page = self.curl()
        if not page:
            return None
        try:
            soup = bs.BeautifulSoup( page )
            return [soup,self.num]
        except:
            print 'type error'
            return None
