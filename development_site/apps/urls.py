from django.conf.urls.defaults import *

urlpatterns = patterns('apps.views',
	url(r'^updateApp/(\d+)$','getAppInfo',name='getAppInfo'),
	url(r'^app/(\d+)$','showAppInfo',name='showAppInfo'),
	url(r'^list','showAppList',name='showAppList'),	
	url(r'^category/(\d+)$','showAppInCategory',name='showAppInCategory'),		
	url(r'^main','main',name='main'),		
)
