from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'settings_time_zone',
        'settings_airdetectordata_unit',
        #'address',
        'last_login',
        'date_joined',
    ]

    def settings_time_zone(self, instance):
        """
        This method allows us to access the time_zone attribute of Settings
        to display in the Django Admin.
        """
        return instance.settings.time_zone
    settings_time_zone.short_description = 'Time zone'

    def settings_airdetectordata_unit(self, instance):
        """
        This method allows us to access the airdetectordata_unit attribute of Settings
        to display in the Django Admin.
        """
        return instance.settings.airdetectordata_unit
    settings_airdetectordata_unit.short_description = 'airdetectordata unit'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
