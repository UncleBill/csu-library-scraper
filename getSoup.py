#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import BeautifulSoup as bs

class getSoup():
    """docstring for getSoup"""
    def __init__(self, num):
        base = 'http://opac.its.csu.edu.cn/NTRdrBookRetrInfo.aspx?BookRecno='
        self.num = num
        self.url = base + str(num)
        self.soupJar = self.getSoup()

    def curl(self):
        attempts = 0
        page = False
        while attempts < 10:
            try:
                page = urllib2.urlopen(self.url)
                break
            except:
                attempts += 1
        return page

    def getSoup(self):
        page = self.curl()
        if not page:
            return None
        try:
            soup = bs.BeautifulSoup( page )
            return [soup, self.num]
        except TypeError:
            print 'type error'
            return None
