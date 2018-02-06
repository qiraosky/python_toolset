# coding:utf8
import urllib2
import browserType as B_TYPE


def readText(url):
    request = urllib2.Request(url)
    request.add_header("User-Agent",B_TYPE.CHROME_40)
    response = urllib2.urlopen(request)
    return response.getcode(),response.read()