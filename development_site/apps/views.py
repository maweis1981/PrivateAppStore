import urllib
import simplejson as json
import feedparser
import math
from decimal import *
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404,HttpResponse,get_list_or_404
from django.db import models,connection
from apps.models import App,ScreenShots,Vendor,Category,iPadScreenShots,Reviews

from AppStoreReviews import storeReviews

def updateApp(app_id):
    url = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsLookup?country=CN&id=%s' % app_id
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content,"UTF-8"))['results'][0]    
    app = App()
    app.app_id = app_id
    exists = App.objects.filter(app_id=app_id)
    if exists:
        app = exists[0]
        
    app.title = contentObj['trackName']
    app.price = float(contentObj['price'])
    app.icon = contentObj['artworkUrl60']
    app.icon100 = contentObj['artworkUrl100']
    app.icon512 = contentObj['artworkUrl512']
    app.description = contentObj['description']
    # print contentObj['releaseDate'] 2011-02-15T02:52:45Z
    # print datetime.strptime(contentObj['releaseDate'],'%Y-%m-%dT%H:%M:%SZ')
    app.releaseDate = datetime.strptime(contentObj['releaseDate'],'%Y-%m-%dT%H:%M:%SZ')

    app.userRatingCountForCurrentVersion = Decimal(contentObj['userRatingCountForCurrentVersion'])
    app.version = contentObj['version']
    
    primaryGenreId = contentObj['primaryGenreId']
    pc = Category.objects.filter(cate_id = primaryGenreId)
    if not pc:
        primaryCate = Category()
        primaryCate.cate_id = primaryGenreId
        primaryCate.cate_name = contentObj['primaryGenreName']
        primaryCate.save()
        app.primaryCategory = primaryCate
    else:
        app.primaryCategory = pc[0]
    
    secondGenreId = contentObj['genreIds'][1]
    sc = Category.objects.filter(cate_id = secondGenreId)
    if not sc:
        secondCate = Category()
        secondCate.cate_id = secondGenreId
        secondCate.cate_name = contentObj['genres'][1]
        secondCate.save()
        app.secondCategory = secondCate
    else:
        app.secondCategory = sc[0]
        
    app.fileSizeBytes = int(contentObj['fileSizeBytes'])
    app.isGameCenterEnabled = contentObj['isGameCenterEnabled']
    app.trackCensoredName = contentObj['trackCensoredName']
    app.userRatingCount = contentObj['userRatingCount']
    app.trackContentRating = contentObj['trackContentRating']
    app.averageUserRatingForCurrentVersion = float(contentObj['averageUserRatingForCurrentVersion'])
    app.averageUserRating = float(contentObj['averageUserRating'])
    
    # app.supportedDevices = contentObj['']
    deviceSupportStr = ''
    for d in contentObj['supportedDevices']:
        deviceSupportStr = '%s,%s' % (deviceSupportStr,d)
    app.supportedDevices = deviceSupportStr
    
    languageSupport = ''
    for l in contentObj['languageCodesISO2A']:
        languageSupport = '%s,%s' % (languageSupport,l)
    app.languageCodesISO2A = languageSupport
    
    artistId = contentObj['artistId']
    print artistId
    vendors = Vendor.objects.filter(artistId = artistId)
    if not vendors:
        vendor = Vendor()
        vendor.artistId = artistId
        vendor.name = contentObj['artistName']
        vendor.url = contentObj['sellerUrl']
        vendor.seller_name = contentObj['sellerName']
        vendor.save()
    else:
        vendor = vendors[0]
    app.seller = vendor 
    app.save()
        
    for i in contentObj['ipadScreenshotUrls']:
        iPadScreenShot = iPadScreenShots()
        iPadScreenShot.ipad_screenshot_url = i
        iPadScreenShot.app = app
        exists = iPadScreenShots.objects.filter(ipad_screenshot_url=i)
        if not exists:
            iPadScreenShot.save()
        else:
            print 'already saved. need check and update operation.'
        
    for i in contentObj['screenshotUrls']:
        screenShot = ScreenShots()
        screenShot.screenshot_url = i
        screenShot.app = app
        exists = ScreenShots.objects.filter(screenshot_url=i)
        if not exists:
            screenShot.save()
        else:
            print 'already saved. need check and update operation.'
    
    #get reviews from all countries
    reviews = storeReviews(app_id)
    if len(reviews)>0:    
        #single country review
        for country_reviews in reviews:
            if len(country_reviews)>0:
                print 'Country : %s' % country_reviews[1]
                country = country_reviews[1]
                for countryReview in country_reviews[0]:
                    print "%s (%s) %s" % (countryReview['rank'],countryReview["topic"], countryReview["review"])
                    review = Reviews()
                    review.country = country
                    review.rating = int(countryReview['rank'])
                    review.topic = countryReview['topic']
                    review.review = countryReview['review']
                    review.app = app
                    review.save()
    print 'Done'



def getAppInfo(request,app_id):
    url = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsLookup?country=CN&id=%s' % app_id
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content,"UTF-8"))['results'][0]    
    app = App()
    app.app_id = app_id
    exists = App.objects.filter(app_id=app_id)
    if exists:
        app = exists[0]
        
    app.title = contentObj['trackName']
    app.price = float(contentObj['price'])
    app.icon = contentObj['artworkUrl60']
    app.icon100 = contentObj['artworkUrl100']
    app.icon512 = contentObj['artworkUrl512']
    app.description = contentObj['description']
    # print contentObj['releaseDate'] 2011-02-15T02:52:45Z
    # print datetime.strptime(contentObj['releaseDate'],'%Y-%m-%dT%H:%M:%SZ')
    app.releaseDate = datetime.strptime(contentObj['releaseDate'],'%Y-%m-%dT%H:%M:%SZ')

    app.userRatingCountForCurrentVersion = Decimal(contentObj['userRatingCountForCurrentVersion'])
    app.version = contentObj['version']
    
    primaryGenreId = contentObj['primaryGenreId']
    pc = Category.objects.filter(cate_id = primaryGenreId)
    if not pc:
        primaryCate = Category()
        primaryCate.cate_id = primaryGenreId
        primaryCate.cate_name = contentObj['primaryGenreName']
        primaryCate.save()
        app.primaryCategory = primaryCate
    else:
        app.primaryCategory = pc[0]
    
    secondGenreId = contentObj['genreIds'][1]
    sc = Category.objects.filter(cate_id = secondGenreId)
    if not sc:
        secondCate = Category()
        secondCate.cate_id = secondGenreId
        secondCate.cate_name = contentObj['genres'][1]
        secondCate.save()
        app.secondCategory = secondCate
    else:
        app.secondCategory = sc[0]
        
    app.fileSizeBytes = int(contentObj['fileSizeBytes'])
    app.isGameCenterEnabled = contentObj['isGameCenterEnabled']
    app.trackCensoredName = contentObj['trackCensoredName']
    app.userRatingCount = contentObj['userRatingCount']
    app.trackContentRating = contentObj['trackContentRating']
    app.averageUserRatingForCurrentVersion = float(contentObj['averageUserRatingForCurrentVersion'])
    app.averageUserRating = float(contentObj['averageUserRating'])
    
    # app.supportedDevices = contentObj['']
    deviceSupportStr = ''
    for d in contentObj['supportedDevices']:
        deviceSupportStr = '%s,%s' % (deviceSupportStr,d)
    app.supportedDevices = deviceSupportStr
    
    languageSupport = ''
    for l in contentObj['languageCodesISO2A']:
        languageSupport = '%s,%s' % (languageSupport,l)
    app.languageCodesISO2A = languageSupport
    
    artistId = contentObj['artistId']
    print artistId
    vendors = Vendor.objects.filter(artistId = artistId)
    if not vendors:
        vendor = Vendor()
        vendor.artistId = artistId
        vendor.name = contentObj['artistName']
        vendor.url = contentObj['sellerUrl']
        vendor.seller_name = contentObj['sellerName']
        vendor.save()
    else:
        vendor = vendors[0]
        
    app.seller = vendor
    # print app.app_id
    #  print app.title
    #  print app.price
    #  print app.icon
    #  print app.icon100
    #  print app.icon512
    #  print app.description
    #  print app.releaseDate
    #  print app.version
    #  print app.primaryCategory
    #  print app.secondCategory
    #  print app.fileSizeBytes
    #  print app.isGameCenterEnabled
    #  print app.trackCensoredName
    #  print app.supportedDevices
    #  print app.languageCodesISO2A      
    app.save()
        
    for i in contentObj['ipadScreenshotUrls']:
        iPadScreenShot = iPadScreenShots()
        iPadScreenShot.ipad_screenshot_url = i
        iPadScreenShot.app = app
        exists = iPadScreenShots.objects.filter(ipad_screenshot_url=i)
        if not exists:
            iPadScreenShot.save()
        else:
            print 'already saved. need check and update operation.'
        
    for i in contentObj['screenshotUrls']:
        screenShot = ScreenShots()
        screenShot.screenshot_url = i
        screenShot.app = app
        exists = ScreenShots.objects.filter(screenshot_url=i)
        if not exists:
            screenShot.save()
        else:
            print 'already saved. need check and update operation.'
    
    #get reviews from all countries
    reviews = storeReviews(app_id)
    if len(reviews)>0:    
        #single country review
        for country_reviews in reviews:
            if len(country_reviews)>0:
                print 'Country : %s' % country_reviews[1]
                country = country_reviews[1]
                for countryReview in country_reviews[0]:
                    print "%s (%s) %s" % (countryReview['rank'],countryReview["topic"], countryReview["review"])
                    review = Reviews()
                    review.country = country
                    review.rating = int(countryReview['rank'])
                    review.topic = countryReview['topic']
                    review.review = countryReview['review']
                    review.app = app
                    review.save()
    return HttpResponse('done')
    
    
def showAppInfo(request,app_id):
    app = App.objects.filter(app_id=app_id)[0]
    for s in app.screenshots.all():
        print s
    return render_to_response("apps/app.html",locals())
    
def showAppList(request):
    categories = Category.objects.all()
    apps = App.objects.all().order_by('-createDate')
    return render_to_response("apps/list.html",locals())
    
    
def showAppInCategory(request,category_id):
    categories = Category.objects.all()
    category = Category.objects.filter(cate_id=category_id)[0]
    apps = category.primary_category_apps.all()
    return render_to_response("apps/category.html",locals())
    
    
def main(request):
    return render_to_response("apps/main.html",locals())
    