from django.db import models
from djangotoolbox.fields import ListField

class Category(models.Model):
    cate_id = models.IntegerField()
    cate_name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return '%s' % self.cate_name

# class DevicesSupport(models.Model):
#     device_name = models.CharField(max_length=512)
# 
# class LanguageSupport(models.Model):
#     language = models.CharField(max_length=20)
    
class Vendor(models.Model):
    artistId = models.IntegerField()
    name = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    seller_name = models.CharField(max_length=512)
    def __unicode__(self):
        return '%s' % self.seller_name
    


# Create your models here.
class App(models.Model):
    app_id = models.IntegerField()
    title = models.CharField(max_length=512)
    price = models.FloatField()
    icon = models.CharField(max_length=512)
    icon100 = models.CharField(max_length=512)
    icon512 = models.CharField(max_length=512)
    description = models.TextField()
    releaseDate = models.DateTimeField()
    userRatingCountForCurrentVersion = models.IntegerField()
    version = models.CharField(max_length=10)
    primaryCategory = models.ForeignKey(Category,related_name='primary_category_apps')
    secondCategory = models.ForeignKey(Category,related_name='second_category_apps')
    fileSizeBytes = models.IntegerField()
    isGameCenterEnabled = models.BooleanField()
    trackCensoredName = models.CharField(max_length=512)
    userRatingCount = models.IntegerField()
    trackContentRating = models.CharField(max_length=5) # content rating for adult
    averageUserRatingForCurrentVersion = models.FloatField()
    averageUserRating = models.FloatField()
    seller = models.ForeignKey(Vendor,related_name='vendor_apps')
    supportedDevices = models.CharField(max_length=512)
    languageCodesISO2A = models.CharField(max_length=512)     
    
    createDate = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s' % self.title
    
class ScreenShots(models.Model):
    screenshot_url = models.CharField(max_length=512)
    app = models.ForeignKey(App,related_name='screenshots')

class iPadScreenShots(models.Model):
    ipad_screenshot_url = models.CharField(max_length=512)
    app = models.ForeignKey(App,related_name='ipad_screenshots')
    
class Reviews(models.Model):
    app = models.ForeignKey(App,related_name='app_comments')
    country = models.CharField(max_length=50)
    rating = models.IntegerField()
    topic = models.CharField(max_length=512)
    review = models.TextField()
    
    

    
