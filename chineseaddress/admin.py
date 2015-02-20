# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import *

class UnidentifiedListFilter(SimpleListFilter):
    title = 'unidentified'
    parameter_name = 'unidentified'

    def lookups(self, request, model_admin):
        return (('unidentified', 'unidentified'),)

    def queryset(self, request, queryset):
        if self.value() == 'unidentified':
            return queryset.filter(city=None)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code')

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_fields = 'name'

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_fields = 'name'

@admin.register(DistrictCounty)
class DistrictCountyAdmin(admin.ModelAdmin):
    search_fields = ('name', 'postal_code')

@admin.register(VillageTown)
class VillageTownAdmin(admin.ModelAdmin):
    search_fields = ('name', 'postal_code')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'street_number',
        'villagetown',
        'latitude',
        'longitude',
    ]
