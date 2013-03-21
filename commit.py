#!/usr/bin/python
# -*- coding: utf-8 -*-
class commit():
    """docstring for commit"""
    def __init__(self,db_conn):
        super(commit, self).__init__()
        self.db_con = db_con

    def committer(self.booklist):
        _bl = booklist
        totalCommit += len( _bl )
        if len( _bl ) == 0:
            return
        #dbCommitter( libConn, _bl )
        commit2db()
        l = len( _bl )
        print '>>commit!(',l,'books )'
        self.booklist = []

        print time.ctime()
        print 'total commit',totalCommit
        print 'total failed',totalFaileds
        print 'since last time', time.time() - self.last_time

        self.last_time = time.time()

    def commit2db(self):
        _con = self.db_con
        kl = keyslit
        _bl = self.booklist
        for item in _bl:
            keys_tuple = tuple(  item[i] for i in kl )
            conn.execute( insertScript ,keys_tuple )
            _infos_list = item[u'info']
            for _i in _infos_list:
                print _i[u'RECNO']
                info_value_tuple = tuple( _i[i] for i in entries )
                conn.execute( infoInsertScript,info_value_tuple )
        _con.commit()
