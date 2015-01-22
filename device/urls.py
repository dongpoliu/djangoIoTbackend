# -*- coding: UTF-8 -*-

from django.views.generic import RedirectView
from .views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', device_home, name='device_home'),
)
