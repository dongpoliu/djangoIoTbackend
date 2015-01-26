# coding: utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'device', views.DeviceViewSet)


urlpatterns = patterns('',
    #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),  
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^manage/', include(admin.site.urls)),        
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
