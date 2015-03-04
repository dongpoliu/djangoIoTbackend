# -*- coding: UTF-8 -*-
from django.contrib import admin

from accounts.models import UserSettings

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'airdetectordata_unit',
        'time_zone',
        'province',
        'city',
        'districtcounty',
        'address',
        'modified',
        'created',
    ]

admin.site.register(UserSettings, UserSettingsAdmin)
