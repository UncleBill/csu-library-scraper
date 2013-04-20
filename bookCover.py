import urllib2
import re
import sqlite3

from xml import sax

__DATABASE__ = ""       # TODO: add database
__BASEURL__ = 'http://opac.its.csu.edu.cn/NTRdrBookRetrAjaxImage.aspx?ListISBN=%s&BigImage=1'

class bookCover():
    """fetch book cover image url by isbn code"""

    def __init__( self, isbn ):
        """initialize database, base url, .etc"""
        self.con = sqlite3.connect( __DATABASE__ )
        self.base_url = __BASEURL__
        self.isbn = isbn
        self.xml = self.get_xml()
        self.urls = self.parse_xml()     # what we what
        self.commit2db()                # Done here

    def get_xml( self ):
        """fetch xml content"""
        _url = self.base_url % self.isbn
        _req = urllib2.urlopen( _url )
        _xml = _req.read()
        return _xml

    def parse_xml( self ):
        """parse xml ,return url"""
        # TODO: parse xml
        return _urls

    def commit2db( self ):
        """commit to database"""
        _urls = self.urls
        _script = ""       # TODO: commit script
        self.con.execute( _script % _url )
