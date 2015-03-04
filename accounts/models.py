# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from timezone_field import TimeZoneField
from model_utils.models import TimeStampedModel
from chineseaddress.models import  *
from .util import PROVINCE_CHOICES
from django.forms import ModelForm
from air.models import *

class UserSettings(TimeStampedModel):
    """
    Model to store additional user settings and preferences. Extends User
    model.
    """
    user                              = models.OneToOneField(User, related_name='settings')
    time_zone                   = TimeZoneField(default=settings.TIME_ZONE)
    province                      = models.ForeignKey(Province) 
    city                               = models.ForeignKey(City) 
    districtcounty              = models.ForeignKey(DistrictCounty) 
    address                       = models.CharField(_(u'地址'),max_length=60)
    airdetectordata_unit = models.ForeignKey(Unit, null=False, blank=False, default=1)    
    default_category        = models.ForeignKey(Category, null=True)
    airdetectordata_low   = models.PositiveIntegerField( null=False, blank=False, default=50)
    airdetectordata_high  = models.PositiveIntegerField( null=False, blank=False, default=99)
    airdetectordata_target_min = models.PositiveIntegerField( null=False,  blank=False, default=30)
    airdetectordata_target_max = models.PositiveIntegerField( null=False, blank=False, default=50)

    class Meta:
        verbose_name_plural = u'用户设定'

    def username(self):
        return self.user.username
    
    username.admin_order_field = 'user__username'

