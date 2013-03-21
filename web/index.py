#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
import sqlite3
import urlparse

urls = (
        '/all','index'
        ,'/ctx','ctx'
        )

render = web.template.render('templates/')
class index:
    """ Index """
    def GET(self):
        db = sqlite3.connect('../library.new.db')
        parsed_url = urlparse.urlparse( web.ctx.fullpath )
        query = dict(urlparse.parse_qsl( parsed_url.query ))
        start = int(query['start'])
        sql = "select * from books where id >= %s and id < %s"%(start,start+50)
        data = db.execute(sql).fetchall()
        return render.index( data,(start,start+50) )

def connetdb( db ):
    return sqlite3.connect( db )

if __name__ == '__main__':
    app = web.application( urls,globals() )
    app.run()
