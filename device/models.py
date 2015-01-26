# -*- coding: UTF-8 -*-
import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

#django-location-field
#from geolocation.models import Location
#enf of django-location-field


class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)
   
    def __unicode__(self):
        return unicode(self.tag)

class Device(models.Model):
    title = models.CharField(max_length=60, unique=True)
    desc = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag)
    url = models.CharField(max_length=200)
    idsn = models.TextField(max_length=1000)
    ele = models.TextField(max_length=1000)
    #location = models.ForeignKey(Location)
    private = models.BooleanField(default=True)
    route_to = models.TextField(max_length=1000)
    #auth_info = 
    interval = models.IntegerField(default = 0)    
    activate_code = models.TextField(max_length=1000)
    other  = models.TextField(max_length=1000)
   
    slug = models.SlugField(max_length=255)
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    online = models.BooleanField(default=True)
    #datastreams  = models.ForeignKey(Datastream)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Device"

    def __unicode__(self):
        return self.name

    def save(self):
        self.last_update = datetime.datetime.now()
        super(Device, self).save()

   
