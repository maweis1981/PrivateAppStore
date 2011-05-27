#!/usr/bin/env python
# encoding: utf-8
import urllib
import simplejson as json
import feedparser

def getApp(id):
    url = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsLookup?id=%s' % id
    print url
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content,"UTF-8"))
    return contentObj['results'][0]
    # for a in contentObj['results']:
    #     # print a
    #     print '%s,%s,%s' %(a['trackName'],a['sellerName'],a['price'])
    # return contentObj['results'][0]['trackName']

def getNewFreeAppRss():
    url = 'feed://itunes.apple.com/us/rss/newfreeapplications/limit=10/xml'
    feed = feedparser.parse(url)
    return feed['items']


def getTopPaidApps():
    url = 'http://itunes.apple.com/us/rss/toppaidapplications/limit=10/json?partnerId=30&LS_PARAM=http%3A%2F%2Fclick.linksynergy.com%2Ffs-bin%2Fstat%3Fid%3DKQ7PGBcyc0M%26offerid%3D146261%26type%3D3%26subid%3D0%26tmpid%3D1826%26RD_PARM1%3D'
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content,"UTF-8"))
    return contentObj['feed']

def getNewFreeApps():
    url = 'http://itunes.apple.com/us/rss/newfreeapplications/limit=10/json'
    print url
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content,"UTF-8"))
    return contentObj['feed']
    # for a in contentObj['feed']:
    #         print '%s' % (a)


def getAddress():
    url = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch?term=gre%20voca&country=us&entity=software'
    print url
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content,"UTF-8"))
    for a in contentObj['results']:
        print '%s,%s,%s' %(a['trackName'],a['sellerName'],a['price'])
    # return contentObj['results'][0]['trackName']



if __name__ == "__main__":
    getNewFreeAppRss()
    # getNewFreeApps()
    # getAddress()

