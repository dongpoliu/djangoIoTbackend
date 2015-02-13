# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    #url(r'^$', resource_home, name='resource_home'),
    #url(r'^$', device_home, name='device_home'),   
    url(r'^new/$', DeviceCreateView.as_view(),  name='device_new' ),
    url(r'^list/$', DeviceAllListView.as_view(),  name='device_list' ),    
    url(r'^(?P<pk>\d+)/$', DeviceDetailView.as_view(), name='device_detail'),     
)