# -*- coding: UTF-8 -*-
#===============================================================================
# Author: 刘东坡
# File Name: djangoiot/device/models.py
# Revision: 0.1
# Date: 2015-02-01 19:15
# Description: 
#===============================================================================
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models
import datetime
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
#from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

class Category(models.Model):
    id= models.AutoField(primary_key=True)     
    name = models.CharField(_(u'类型'),max_length=60, unique=True)
    desc = models.CharField(_(u'描述'),max_length=500)        
    #slug = models.SlugField(max_length=255)
    thumbnail = models.ImageField(_(u'缩微图'),upload_to='category', null=True, blank=True)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _(u'类型')
        verbose_name_plural = _(u'类型')
        #unique_together = ('name')
        ordering = ['name']
        
    def __unicode__(self):
        return self.name

    def get_absolute_url (self):
        return reverse('device:device_category_home', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        #if not self.slug:
            #self.slug = slugify(self.id)
        super(Category, self).save(*args, **kwargs)

class Marker(models.Model):
    #id= models.AutoField(primary_key=True) 
    name = models.CharField(_(u'位置'),max_length=40)
    geometry = models.PointField(_(u'地图'),srid=4326)  
    geocoded_accuracy = models.IntegerField(_(u'精确度'),null=True, blank=True)
    geocoded_address = models.CharField(_(u'地址'),max_length=256, null=True, blank=True)
    geocoded_lat = models.FloatField(_(u'纬度'))
    geocoded_lon  = models.FloatField(_(u'经度'))    
    desc = models.TextField(_(u'描述'),max_length=1000)      
    #device = models.ForeignKey(Device, verbose_name="设备",null=True, blank=True)        
    objects = models.GeoManager()
   
    class Meta:
        verbose_name = _(u'位置')
        verbose_name_plural = _(u'位置')
        #unique_together = ('name')
        ordering = ['id']

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.geometry.x, self.geometry.y)
  
  
  
    
class Unit(models.Model):
    name = models.CharField(_(u'单位'),unique=True, max_length=6)

    def __unicode__(self):
        return self.name
    
class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating 'created' and 'modified'
    fields.
    """
    created    = models.DateTimeField(auto_now_add=True)
    modified  = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Datastream(TimeStampedModel):
    id= models.AutoField(primary_key=True) 
    value = models.PositiveIntegerField(validators=[MaxValueValidator(54054),MinValueValidator(0)])
    record_date = models.DateField('Date')
    record_time = models.TimeField('Time')
    notes = models.TextField(null=False, blank=True, verbose_name = _(u'备注'))
    #device = models.ForeignKey(Device, verbose_name="设备",null=True, blank=True)       
    tags = TaggableManager(blank=True, help_text=None)

    class Meta:
        verbose_name             = _(u'数据流')
        verbose_name_plural = _(u'数据流')
        ordering = ['id']
        
    def __unicode__(self):
        return str(self.value)


class Device(models.Model):
    id= models.AutoField(primary_key=True) 
    name = models.CharField(_(u'设备'),max_length=60, unique=True)   
    desc = models.CharField(_(u'描述'),max_length=500)    
    thumbnail = models.ImageField(_(u'缩微图'),upload_to='device', null=True, blank=True)    
    
    owner             = models.ForeignKey(User, verbose_name = _(u'用户'))     
    marker           = models.ForeignKey(Marker, verbose_name = _(u'位置'))   
    category         = models.ForeignKey(Category,verbose_name="类型",null=True, blank=True)
    datastream   =  models.ManyToManyField(Datastream, verbose_name="数据流",null=True, blank=True) 
    
    date_created = models.DateField(_(u'创建日期'),null=True, blank=True)
    present           = models.BooleanField(_(u'存在否'),default=True)
    last_updated = models.DateTimeField(_(u'上次更新'),auto_now=True)
    online             = models.BooleanField(_(u'在线'),default=True)    
    objects           = models.GeoManager()
     
    #slug = models.SlugField(max_length=255)
    #idsn = models.TextField(max_length=1000)
    #ele = models.TextField(max_length=1000)     
    #route_to = models.TextField(_(u'连入'),max_length=1000)
    #interval = models.IntegerField(_(u'间隔'),default = 0)    
    #activate_code = models.TextField(_(u'激活码'),max_length=1000)  
    #date_removed = models.DateField(_(u'删除日期'),null=True, blank=True)  
    #other  = models.TextField(_(u'其他'),max_length=1000) 
    #private = models.BooleanField(_(u'私有'),default=True)
    #auth_info = 
    #dbh = models.FloatField(null=True, blank=True) #gets auto-set on save
       
    class Meta:
        verbose_name = _(u'设备')
        verbose_name_plural = _(u'设备')
        unique_together = ('name','desc')
   
    def get_absolute_url(self):
        return reverse('device:device_detail', kwargs={'pk': self.id})
    
    def save(self, *args, **kwargs):
        #if not self.slug:
            #self.slug = slugify(self.name)
        super(Device, self).save(*args, **kwargs)

    def get_lat_lon(self):
        lat_lon = [self.marker.geometry.x, self.marker.geometry.y]
        return  lat_lon






  
