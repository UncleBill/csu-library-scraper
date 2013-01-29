#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import BeautifulSoup as bs

def getSoup( url ):
    page = urllib2.urlopen( url )
    soup = bs.BeautifulSoup( page )
    return soup
