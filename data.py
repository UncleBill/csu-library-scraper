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
# ########################################
store_entries = [
    u'索书号'
    ,u'条形码'
    ,u'登录号'
    ,u'馆藏地点'
    ,u'管藏状态'
    ,u'借出日期'
    ,u'还回日期'
    ,u'流通类型'
    ,u'预约处理'
    ,u'卷册说明'
    ,u'RECNO']
store_script = """insert into bookInfos (
    ,commit_time
    ,call_num
    ,bar_code
    ,login_num
    ,store_loca
    ,store_state
    ,lend_date
    ,return_date
    ,tran_type
    ,order_handle
    ,volumn_info
    ,recno) values ( datetime('now'), ?,?,?,?,?,?,?,?,?,?,? )"""
