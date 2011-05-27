import tornado.ioloop
import tornado.web
import tornado.httpserver

from iTunesAPIs import getNewFreeAppRss,getApp
from robot import viewData

import Queue
appQueue = Queue.Queue(0)
import re

from appObject import AppObject

settings = {'debug' : True}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = viewData()
        objs = []
        
        for i in items:        
            linkUrl = i['link'][0]['attributes']['href']
            app_id = re.findall(r'id(\d+)',linkUrl,re.S)[0]
            
            app = AppObject()
            app.setAppId(app_id)
            app.setTitle(i['title']['label'])
            app.setIcon(i['im:image'][2]['label'])
            objs.append(app)
            
        self.render("templates/main.html",apps = objs)



class AppHandler(tornado.web.RequestHandler):
    def get(self,app_id):
        appContent = getApp(app_id)
 
        app = AppObject()
        app.setAppId(app_id)
        app.setTitle(appContent['trackName'])
        app.setIcon(appContent['artworkUrl60'])
        app.setPrice(appContent['price'])
        app.setDescription(appContent['description'])
        screenshots = []
        for i in appContent['screenshotUrls']:
            screenshots.append(i)
        print screenshots
        app.setScreenshots(screenshots)
        self.render("templates/app.html",app = app)
            
        
application = tornado.web.Application([
    (r'/',MainHandler),
    (r'/app/([0-9]+)',AppHandler),
], **settings)

if __name__ == '__main__':
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    