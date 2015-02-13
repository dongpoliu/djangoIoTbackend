# -*- coding: UTF-8 -*-
#===============================================================================
# Author: 刘东坡
# File Name: djangoiot/device/models.py
# Revision: 0.1
# Date: 2015-02-01 19:15
# Description: 
#===============================================================================
from django.contrib import admin
from devices.models import Device 

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'desc', 'online','thumbnail',)
    #prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    search_fields = ('name', 'desc',)

admin.site.register(Device, DeviceAdmin)
