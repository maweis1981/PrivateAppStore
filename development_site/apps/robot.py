import pymongo
from iTunesAPIs import getTopPaidApps

from pymongo import Connection
from views import updateApp

import os

os.environ["DJANGO_SETTINGS_MODULE"] = "development_site.settings"


def storeData():
    items = getTopPaidApps()
    connection = Connection('localhost', 27017)
    db  = connection['pretty_apps']
    apps = db.apps
    for item in items['entry']:
        print item['title']['label']
        print '-----------------------'
        apps.insert(item)
        
        
def viewData():
    connection = Connection('localhost', 27017)
    db  = connection['pretty_apps']
    apps = db.apps.find().sort('$natural',pymongo.DESCENDING).limit(10)
    return apps
    
    

def getTopPaidApps():
        # url = 'http://itunes.apple.com/us/rss/toppaidapplications/limit=10/json'
    url = 'http://itunes.apple.com/cn/rss/topgrossingapplications/limit=10/genre=6011/json'
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content,"UTF-8"))
    for e in contentObj['feed']['entry']:
        linkUrl = e['link'][0]['attributes']['href']
        app_id = re.findall(r'id(\d+)',linkUrl,re.S)[0]
        print app_id
        updateApp(app_id)
        # urllib.urlopen('http://localhost:8000/apps/updateApp/%s' % app_id)

if __name__ == "__main__":
    getTopPaidApps()
    # getNewFreeApps()
    # getAddress()
