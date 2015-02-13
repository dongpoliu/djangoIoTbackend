# -*- coding: UTF-8 -*-
#===============================================================================
# Author: 刘东坡
# File Name: djangoiot/device/models.py
# Revision: 0.1
# Date: 2015-02-01 19:15
# Description: 
#===============================================================================
from django.db import models
from geoposition.fields import GeopositionField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
 
class Device(models.Model):
    id= models.AutoField(primary_key=True) 
    name = models.CharField(_(u'设备'),max_length=60, unique=True)   
    desc = models.CharField(_(u'描述'),max_length=500)    
    thumbnail = models.ImageField(_(u'缩微图'),upload_to='device', null=True, blank=True)        
    owner             = models.ForeignKey(User, verbose_name = _(u'用户'))     
    date_created = models.DateField(_(u'创建日期'),null=True, blank=True)
    present           = models.BooleanField(_(u'存在否'),default=True)
    last_updated = models.DateTimeField(_(u'上次更新'),auto_now=True)
    online             = models.BooleanField(_(u'在线'),default=True)    
    coordinates   = GeopositionField()  

    class Meta:
        verbose_name = _(u'设备')
        verbose_name_plural = _(u'设备')
        unique_together = ('name','desc')
   
    def get_absolute_url(self):
        return reverse('device:device_detail', kwargs={'pk': self.id})
    
    def save(self, *args, **kwargs):
        super(Device, self).save(*args, **kwargs)








  
