# -*- coding: UTF-8 -*-
from datetime import datetime

from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response,render,redirect
from django.core.urlresolvers import reverse_lazy, reverse
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, RedirectView
from braces.views import SetHeadlineMixin

from .models import Device 
from .forms import DeviceCreateForm, DeviceUpdateForm 
  
def index (request):
    #return render_to_response('index.html', locals(), context_instance=RequestContext(request))
    return redirect("/map/")  

def map (request):
    user = request.user
    devices = Device.objects.filter(owner__username=user)
    #markers = Marker.objects.filter(device__name=user).order_by('name')

    ctx = {
            'devices': devices,
            #'markers':markers,
        }        
    
    return render_to_response('devices/map.html', ctx, context_instance=RequestContext(request))
   
class DeviceAllListView(SetHeadlineMixin, ListView):
    context_object_name = 'devices'
    template_name = 'devices/device_list.html'
    paginate_by = 12

    def get_queryset(self):
        devices = Device.objects.all()
        self.headline = 'All Devices'
        return devices

class DeviceCreateView(LoginRequiredMixin, SetHeadlineMixin, CreateView):
    form_class = DeviceCreateForm
    template_name = 'devices/device_create.html'
    model = Device
    headline = '添加新设备'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(DeviceCreateView, self).form_valid(form)

class DeviceDetailView(LoginRequiredMixin,SetHeadlineMixin, DetailView):
    model = Device
    context_object_name = 'device'
    template_name = 'devices/device_detail.html'

    def get_object(self):
        device = super(DeviceDetailView, self).get_object()
        self.headline = unicode(device.name) 
        return device

    def get_context_data(self, **kwargs):
        context = super(DeviceDetailView, self).get_context_data(**kwargs)
        return context


  
