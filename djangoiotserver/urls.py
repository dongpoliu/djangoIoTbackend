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
    url(r'^$', 'core.views.home', name='dashboard'),
    url(r'^map$', 'core.views.map', name='map'),
    url(r'^data$', 'core.views.data', name='data'),
    url(r'^about/$', 'core.views.about', name='about'),
    url(r'^help/$', 'core.views.help', name='help'),
    url(r'^support/$', 'core.views.support', name='support'),
    url(r'^explore/$', 'core.views.explore', name='explore'),
    url(r'^signup/$', 'auth.views.signup', name='signup'),
    url(r'^signin/$', 'auth.views.signin', name='signin'),
    url(r'^signout/$', 'auth.views.signout', name='signout'),
    url(r'^reset/$', 'auth.views.reset', name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'auth.views.reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'auth.views.success', name='success'),     
    url(r'^settings/', include('settings.urls', namespace='settings')),    
    #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),  
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^manage/', include(admin.site.urls)),  
    url(r'^(?P<username>[^/]+)/$', 'device.views.device_home', name='device_home'),   
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
