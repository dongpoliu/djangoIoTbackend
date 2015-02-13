# coding: utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'devices.views.index', name='index'),
    url(r'^map/$', 'devices.views.map', name='map'),
    url(r'^device/', include('devices.urls', namespace='devices')),
    url(r'^about/$', 'core.views.about', name='about'),
    url(r'^help/$', 'core.views.help', name='help'),
    url(r'^support/$', 'core.views.support', name='support'),
    url(r'^explore/$', 'core.views.explore', name='explore'),
    url(r'^signup/$', 'userauth.views.signup', name='signup'),
    url(r'^signin/$', 'userauth.views.signin', name='signin'),
    url(r'^signout/$', 'userauth.views.signout', name='signout'),
    url(r'^reset/$', 'userauth.views.reset', name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'userauth.views.reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'userauth.views.success', name='success'),     
    url(r'^settings/', include('settings.urls', namespace='settings')),
    url(r'^profile/$', 'settings.views.profile', name='profile'),      
    url(r'^password/$', 'settings.views.password', name='password'),   
    #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),  
    #url(r'^api/', include(router.urls)),
    url(r'^manage/', include(admin.site.urls)),  
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



