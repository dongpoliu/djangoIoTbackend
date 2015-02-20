# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignObject, ReverseSingleRelatedObjectDescriptor
from django.utils.encoding import python_2_unicode_compatible

import logging
logger = logging.getLogger(__name__)

# Python 3 fixes.
import sys
if sys.version > '3':
    long = int
    basestring = (str, bytes)
    unicode = str

#__all__ = ['Country', 'State', 'Locality', 'Address', 'AddressField']
__all__ = ['Country', 'Province', 'City','DistrictCounty','VillageTown', 'Address', 'AddressField']

class InconsistentDictError(Exception):
    pass

def _to_python(value):
    raw = value.get('raw', '')
    country = value.get('country', '')
    country_code = value.get('country_code', '')
    province = value.get('province', '')
    city = value.get('city', '')
    districtcounty = value.get('districtcounty', '')
    villagetown  = value.get('villagetown', '')
    postal_code = value.get('postal_code', '')
    street_number = value.get('street_number', '')
    route = value.get('route', '')
    #formatted = value.get('formatted', '')
    latitude = value.get('latitude', None)
    longitude = value.get('longitude', None)

    # If there is no value (empty raw) then return None.
    if not raw:
        return None

    # If we have an inconsistent set of value bail out now.
    if (country or province or city or districtcounty ) and not (country and province and city and districtcounty):
        raise InconsistentDictError

    # Handle the country.
    try:
        country_obj = Country.objects.get(name=country)
    except Country.DoesNotExist:
        if country:
            country_obj = Country.objects.create(name=country, code=country_code)
        else:
            country_obj = None

    # Handle the province.
    try:
        province_obj = Province.objects.get(name=province, country=country_obj)
    except Province.DoesNotExist:
        if province:
            province_obj = Province.objects.create(name=province, country=country_obj)
        else:
            province_obj = None

    # Handle the city.
    try:
        city_obj = City.objects.get(name=city, province=province_obj)
    except City.DoesNotExist:
        if City:
            city_obj = City.objects.create(name=city, province=province_obj)
        else:
            city_obj = None

    # Handle the districtcounty.
    try:
        districtcounty_obj = DistrictCounty.objects.get(name=districtcounty, city=city_obj)
    except DistrictCounty.DoesNotExist:
        if DistrictCounty:
            districtcounty_obj = DistrictCounty.objects.create(name=districtcounty, city=city_obj)
        else:
            districtcounty_obj = None

    # Handle the villagetown.
    try:
        villagetown_obj = VillageTown.objects.get(name=districtcounty, districtcounty=districtcounty_obj)
    except VillageTown.DoesNotExist:
        if VillageTown:
            villagetown_obj = VillageTown.objects.create(name=villagetown, postal_code=postal_code, districtcounty=districtcounty_obj)
        else:
            villagetown_obj = None

    # Handle the address.
    try:
        if not (street_number or route or districtcounty):
            address_obj = Address.objects.get(raw=raw)
        else:
            address_obj = Address.objects.get(
                street_number=street_number,
                route=route,
                villagetown=villagetown_obj
            )
    except Address.DoesNotExist:
        address_obj = Address(
            street_number=street_number,
            route=route,
            #raw=raw,
            villagetown=villagetown_obj,
            #formatted=formatted,
            latitude=latitude,
            longitude=longitude,
        )

        # If "formatted" is empty try to construct it from other values.
        if not address_obj.formatted:
            address_obj.formatted = unicode(address_obj)

        # Need to save.
        address_obj.save()

    # Done.
    return address_obj

##
## Convert a dictionary to an address.
##
def to_python(value):

    # Keep `None`s.
    if value is None:
        return None

    # Is it already an address object?
    if isinstance(value, Address):
        return value

    # If we have an integer, assume it is a model primary key. This is mostly for
    # Django being a cunt.
    elif isinstance(value, (int, long)):
        return value

    # A string is considered a raw value.
    elif isinstance(value, basestring):
        obj = Address(raw=value)
        obj.save()
        return obj

    # A dictionary of named address components.
    elif isinstance(value, dict):

        # Attempt a conversion.
        try:
            return _to_python(value)
        except InconsistentDictError:
            return Address.objects.create(raw=value['raw'])

    # Not in any of the formats I recognise.
    raise ValidationError('Invalid address value.')

##
## A country.
##
@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(_(u'国家'),max_length=40, unique=True, blank=True)
    code = models.CharField(max_length=2, blank=True) # not unique as there are duplicates (IT)

    class Meta:
        verbose_name_plural =_(u'国家')
        ordering = ('name',)

    def __str__(self):
        return u'%s'%(self.name or self.code)

##
## A province.  
##
@python_2_unicode_compatible
class Province(models.Model):
    name = models.CharField(_(u'省份'),max_length=165, blank=True)
    country = models.ForeignKey(Country, related_name='provinces')

    class Meta:
        verbose_name_plural = u'省份'
        unique_together = ('name', 'country')
        ordering = ('country', 'name')

    def __str__(self):
        txt = self.to_str()
        country = u'%s'%self.country
        if country and txt:
            txt += ', '
        txt += country
        return txt

    def to_str(self):
        return u'%s'%(self.name)

##
## A City (suburb).
##
@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(_(u'城市'),max_length=165, blank=True)
    #postal_code = models.CharField(_(u'邮编'),max_length=10, blank=True)
    province = models.ForeignKey(Province, related_name='cities')

    class Meta:
        verbose_name_plural = u'城市'
        unique_together = ('name', 'province')
        ordering = ('province', 'name')

    def __str__(self):
        txt = u'%s'%self.name
        province = self.province.to_str() if self.province else ''
        if txt and province:
            txt += ', '
        txt += province 
        cntry =u'%s'%(self.province.country if self.province and self.province.country else '')
        if cntry:
            txt += u', %s'%cntry
        return txt

    def to_str(self):
        return u'%s'%(self.name)
##
## A DistrictCounty (suburb).
##
@python_2_unicode_compatible
class DistrictCounty(models.Model):
    name = models.CharField(_(u'区县'),max_length=165, blank=True)
    city = models.ForeignKey(City, related_name='districtcounties')

    class Meta:
        verbose_name_plural = u'区县'
        unique_together = ('name', 'city')
        ordering = ('city', 'name')

    def __str__(self):
        txt = u'%s'%self.name
        city = self.city.to_str() if self.city else ''
        if txt and city:
            txt += ', '
        txt += city       
        province = self.city.province.to_str() if self.city.province else ''        
        if txt and province:
            txt += ', '
        txt += province 
        cntry =u'%s'%(self.city.province.country if self.city.province and self.city.province.country else '')        
        
        if cntry:
            txt += u', %s'%cntry
        return txt

    def to_str(self):
        return u'%s'%(self.name)

##
## A VillageTown (suburb).
##
@python_2_unicode_compatible
class VillageTown(models.Model):
    name = models.CharField(_(u'街道乡镇'),max_length=165, blank=True)
    districtcounty = models.ForeignKey(DistrictCounty, related_name='villagetowns')
    postal_code = models.CharField(_(u'邮编'),max_length=10, blank=True)    

    class Meta:
        verbose_name_plural = u'街道乡镇'
        unique_together = ('name', 'districtcounty')
        ordering = ('districtcounty', 'name')

    def __str__(self):
        txt = u'%s'%self.name
        districtcounty = self.districtcounty.to_str() if self.districtcounty else ''
        if txt and districtcounty:
            txt += ', '
        txt += districtcounty        
          
        city = self.districtcounty.city.to_str() if self.districtcounty.city else ''
        if txt and city:
            txt += ', '
        txt += city              
                  
        province = self.districtcounty.city.province.to_str() if self.districtcounty.city.province else ''        
        if txt and province:
            txt += ', '
        txt += province         
        
        cntry =u'%s'%(self.districtcounty.city.province.country if self.districtcounty.city.province and self.districtcounty.city.province.country else '')
        if cntry:
            txt += u', %s'%cntry
        return txt

    def to_str(self):
        return u'%s'%(self.name)
    
##
## An address. If for any reason we are unable to find a matching
## decomposed address we will store the raw address string in `raw`.
##
@python_2_unicode_compatible
class Address(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(_(u'名称'),max_length=165, blank=True)    
    street_number = models.CharField(_(u'详细地址'),max_length=20, blank=True)
    route = models.CharField(_(u'路线'),max_length=100, blank=True)
    villagetown = models.ForeignKey(VillageTown, related_name='addresses', blank=True, null=True) 
    latitude = models.FloatField(_(u'纬度'),blank=True, null=True)
    longitude = models.FloatField(_(u'经度'),blank=True, null=True)

    class Meta:
        verbose_name_plural = _(u'地址')
        ordering = ('villagetown', 'route', 'street_number')

    def __str__(self):
        txt = '%s'%self.name
        villagetown = self.villagetown.to_str() if self.villagetown else '' 
        if self.street_number:
            txt = u'%s'%self.street_number
        if self.route:
            if txt:
                txt += ' %s'%self.route
        #districtcounty = u'%s'%self.districtcounty
        if txt and villagetown:
            txt += ', '
        txt += villagetown
        return txt

    def clean(self):
        if not self.villagetown:
            raise ValidationError('Addresses may not have a blank `villagetown` field.')

    def as_dict(self):
        ad = dict(
            street_number=self.street_number,
            route=self.route,
            latitude=self.latitude if self.latitude else '',
            longitude=self.longitude if self.longitude else '',
        )
        if self.villagetown:
            ad['villagetown'] = self.villagetown.name
            ad['postal_code'] = self.villagetown.districtcounty.postal_code
            if self.villagetown.districtcounty:
                ad['districtcounty'] = self.districtcounty.name                                       
                if self.villagetown.districtcounty.city:
                    ad['city'] = self.villagetown.districtcounty.city.name            
                    if self.villagetown.districtcounty.city.province:
                        ad['province'] = self.villagetown.districtcounty.city.province.name
                        if self.villagetown.districtcounty.city.province.country:
                            ad['country'] = self.villagetown.districtcounty.city.province.country.name
                            ad['country_code'] = self.villagetown.districtcounty.city.province.country.code
        return ad

class AddressDescriptor(ReverseSingleRelatedObjectDescriptor):

    def __set__(self, inst, value):
        super(AddressDescriptor, self).__set__(inst, to_python(value))

##
## A field for addresses in other models.
##
class AddressField(models.ForeignKey):
    description = 'An address'

    def __init__(self, **kwargs):
        kwargs['to'] = Address
        super(AddressField, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(ForeignObject, self).contribute_to_class(cls, name, virtual_only=virtual_only)
        setattr(cls, self.name, AddressDescriptor(self))

    # def deconstruct(self):
    #     name, path, args, kwargs = super(AddressField, self).deconstruct()
    #     del kwargs['to']
    #     return name, path, args, kwargs

    def formfield(self, **kwargs):
        from .forms import AddressField as AddressFormField
        defaults = dict(form_class=AddressFormField)
        defaults.update(kwargs)
        return super(AddressField, self).formfield(**defaults)
