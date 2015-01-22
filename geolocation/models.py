# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from django.db import models
from django.template.defaultfilters import slugify
from location_field.models.plain import PlainLocationField

class Location(models.Model):
    city = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    plain_location = PlainLocationField(based_fields=[city], zoom=7)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)    
    
    class Meta:
        ordering = ['city',]

    def __unicode__(self):
        return self.city

    def get_absolute_url(self):
        return reverse('xxxx', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)    


