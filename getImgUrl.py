import urllib2
import re

def getXml( isbn ):
    xmlUrl = 'http://opac.its.csu.edu.cn/NTRdrBookRetrAjaxImage.aspx?ListISBN=%s&BigImage=1'%isbn
    xmlreq = urllib2.urlopen( xmlUrl )
    xmltext = xmlreq.read()
    return xmltext
def getImgUrl( xmltext ):
    url = re.findall( 'http:.*\d+.jpg', xmltext )
    return url[0]
