from django.contrib import admin
from device.models import Device

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'activate_code','online',)
    prepopulated_fields = {'url': ('title',)}
    list_filter = ('title',)
    search_fields = ('title', 'desc', 'activate_code','online',)

admin.site.register(Device, DeviceAdmin)

