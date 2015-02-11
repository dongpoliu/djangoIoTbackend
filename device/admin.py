# -*- coding: UTF-8 -*-
#===============================================================================
# Author: 刘东坡
# File Name: djangoiot/device/models.py
# Revision: 0.1
# Date: 2015-02-01 19:15
# Description: 
#===============================================================================
from django.contrib import admin
from device.models import Device, Marker,Datastream,Category

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'desc', 'online','category','thumbnail','marker')
    #prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    search_fields = ('name', 'desc',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'thumbnail')
    #prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    search_fields =('name', 'desc', 'thumbnail',)

class MarkerAdmin(admin.ModelAdmin):
    default_lon = -93
    default_lat = 27
    default_zoom = 15    
    list_display = ('name', 'geometry')
    exclude = ('geocoded_lat','geocoded_lon')
    list_filter = ('name',)
    search_fields = [('name'),]

class DatastreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'value','record_date','record_time','notes')
    list_filter = ('value',)
    search_fields = [('value'),]

admin.site.register(Device, DeviceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Marker, MarkerAdmin)
admin.site.register(Datastream, DatastreamAdmin)
