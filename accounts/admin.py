from django.contrib import admin

from accounts.models import UserSettings

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'time_zone',
        'modified',
        'created',
    ]


admin.site.register(UserSettings, UserSettingsAdmin)
