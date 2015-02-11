from datetime import datetime, timedelta
from django.utils.timesince import timesince
from urlparse import urlparse
from django.core.urlresolvers import reverse
from django import template

from django.utils.safestring import mark_safe
from django.template import Library

import json

from device.models import Category

register = template.Library()

@register.tag
def get_category (request):
    categories = Category.objects.filter(device__name__isnull=False).distinct().order_by('-id')   
    return categories

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter(is_safe=True)
def remove_point(obj):   
    newobj = obj.replace('POINT','')    ## here's the mathematical operation
    newobj = list(newobj)
    return newobj

@register.filter()
def to_int(value):
    return int(value)

@register.filter(name='json')
def _json(obj):
  #remember to make sure the contents are actually safe before you use this filter!
  return safestring.mark_safe(json.dumps(obj))