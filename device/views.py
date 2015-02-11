# -*- coding: UTF-8 -*-
from datetime import datetime
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.db import transaction

#ip part
from ipware.ip import get_ip
import ipgetter


#GEOIP
from django.contrib.gis.geoip import GeoIP

from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response,render
from django.core.urlresolvers import reverse_lazy, reverse
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, RedirectView
from braces.views import SetHeadlineMixin

from .models import Device, Marker, Category
from .forms import DeviceCreateForm, DeviceUpdateForm 

def device_home(request):
    categories = Category.objects.filter(device__name__isnull=False).distinct().order_by('name')    

    if request.session.get('no_category', False):
        messages.warning(request, 'It seems you are not following any category. Follow no_categories by clicking on it below and get personalized recommendations')
        request.session['no_category'] = False

    ctx = {
            'categories': categories,
        }
    return render_to_response('device/device_home.html',          ctx, context_instance=RequestContext(request))    

def category_home(request, id):
    current_category = get_object_or_404(Category, id=id)
    headline =  current_category.name 
    categories = Category.objects.filter(device__name__isnull=False).distinct().order_by('name')    

    ctx = {
        'current_category': current_category,
        'headline': headline,
        'categories': categories,
    }

    return render_to_response('device/category_home.html', ctx, context_instance=RequestContext(request))


 
def devicelist(request):
    devices = Device.objects.order_by('name')
    if request.session.get('no_device', False):
        messages.warning(request, 'It seems you are having any device.')
        request.session['no_device'] = False

    ctx = {
             'devices': devices,
        }
    return render_to_response('device/device_list.html', ctx, context_instance=RequestContext(request))    
    
class DeviceAllListView(SetHeadlineMixin, ListView):
    context_object_name = 'devices'
    template_name = 'device/device_list.html'
    paginate_by = 12

    def get_queryset(self):
        devices = Device.objects.all()
        self.headline = 'All Devices'
        return devices

class DeviceCreateView(LoginRequiredMixin, SetHeadlineMixin, CreateView):
    form_class = DeviceCreateForm
    template_name = 'device/device_create.html'
    model = Device
    headline = '添加新设备'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(DeviceCreateView, self).form_valid(form)

class DeviceDetailView(LoginRequiredMixin,SetHeadlineMixin, DetailView):
    model = Device
    context_object_name = 'device'
    template_name = 'device/device_detail.html'

    def get_object(self):
        device = super(DeviceDetailView, self).get_object()
        self.headline = unicode(device.name) 
        return device

    def get_context_data(self, **kwargs):
        context = super(DeviceDetailView, self).get_context_data(**kwargs)
        return context

def get_client_ip1(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip

def get_external_ip():
    external_ip = ipgetter.myip()
    #print external_ip 
    return  external_ip


def get_client_ip2(request):
    client_ip2 = get_ip(request)
    if client_ip2 is not None:
        print "we have an IP address for user"
        return client_ip2
    else:
        print "we don't have an IP address for user"
        return None

def get_lat_lon():
    external_ip = get_external_ip()
    g = GeoIP()
    lat_lon = g.lat_lon(external_ip)
    lat_lon = list(lat_lon)
    return lat_lon
  
def map(request):
    user = request.user
    devices = Device.objects.filter(owner__username=user)
    lat_lon = get_lat_lon
    #markers = Marker.objects.filter(device__name=user).order_by('name')

    #Check various session values for user details and show appropriate info
    if request.session.get('no_device', False):
        messages.warning(request, 'It seems you are having any device.')
        request.session['no_device'] = False

    ctx = {
            'devices': devices,
            'lat_lon':lat_lon,
            #'markers':markers,
        }
    return render_to_response('device/map2.html', ctx, context_instance=RequestContext(request))

#@transaction.commit_manually
#def flush_transaction():
    """
    Flush the current transaction so we don't read stale data

    Use in long running processes to make sure fresh data is read from
    the database.  This is a problem with MySQL and the default
    transaction mode.  You can fix it by setting
    "transaction-isolation = READ-COMMITTED" in my.cnf or by calling
    this function at the appropriate moment
    """
    #transaction.commit()