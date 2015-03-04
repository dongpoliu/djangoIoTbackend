# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.text import Truncator
from .models import AirCleaner, AirDetector, AirDetectorData, Category, Unit

class AirCleanerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'owner',
        'address',
        'date_created',
        'last_updated',
        'notes_truncated',
        'tag_list',
        # 'coordinates',
        'on_off',
        'present',
        'online',
        'thumbnail',
    ]

    list_filter = [
        'owner',
        'date_created',
    ]

    def notes_truncated(self, obj):
        return Truncator(obj.notes).chars(75)
    notes_truncated.admin_order_field = 'notes'
    notes_truncated.short_description = 'Notes'

    def tag_list(self, obj):
        """
        Retrieve the tags separated by comma.
        """
        return ', '.join([t.name for t in obj.tags.all()])
    tag_list.short_description = 'Tags'

class AirDetectorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'owner',
        'associated',
        'address',
        'date_created',
        'last_updated',
        'notes_truncated',
        'tag_list',
        #'coordinates',
        'on_off',
        'present',
        'online',
        'thumbnail',
    ]

    list_filter = [
        'owner',
        'date_created',
    ]

    def notes_truncated(self, obj):
        return Truncator(obj.notes).chars(75)
    notes_truncated.admin_order_field = 'notes'
    notes_truncated.short_description = 'Notes'

    def tag_list(self, obj):
        """
        Retrieve the tags separated by comma.
        """
        return ', '.join([t.name for t in obj.tags.all()])
    tag_list.short_description = 'Tags'

class AirDetectorDataAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'value',
        'airdetector',
        'record_date',
        'record_time',
        'notes',
    ]
    list_filter = [
        'id',
        'value',
    ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

class UnitAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

admin.site.register(Unit,UnitAdmin)   
admin.site.register(Category,CategoryAdmin)   
admin.site.register(AirDetectorData,AirDetectorDataAdmin)
admin.site.register(AirCleaner, AirCleanerAdmin)
admin.site.register(AirDetector, AirDetectorAdmin)
