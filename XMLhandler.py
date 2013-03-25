import urllib2

class XMLhandler():
    """A base class for bookCover and storeInfo"""
    def __init__( self, isbn ):
        self.isbn = isbn
        self.xml = self.get_xml()

    def get_xml( self ):
        """fetch xml content"""
        _url = self.base_url % self.isbn
        _req = urllib2.urlopen( _url )
        _xml = _req.read()
        return _xml
