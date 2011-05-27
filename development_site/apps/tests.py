"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from views import updateApp


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    
    def test_data_spider(self):
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
