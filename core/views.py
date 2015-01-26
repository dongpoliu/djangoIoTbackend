# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from device.models import Device 
from datetime import datetime

def get_following_devices(user):
    devices = []    
    return devices

def home(request):
    if request.user.is_authenticated():
        devices = get_following_devices(request.user)
        context = RequestContext(request, { 'devices': devices, })
        return render_to_response('core/home.html', context)
    else:
        context = RequestContext(request)
        return render_to_response('core/cover.html', context)

def map(request):
    if request.user.is_authenticated():
        devices = get_following_devices(request.user)
        context = RequestContext(request, { 'devices': devices, })
        return render_to_response('core/home.html', context)
    else:
        context = RequestContext(request)
        return render_to_response('core/cover.html', context)

def data(request):
    if request.user.is_authenticated():
        devices = get_devices(request.user)
        context = RequestContext(request, { 'devices': devices, })
        return render_to_response('core/home.html', context)
    else:
        context = RequestContext(request)
        return render_to_response('core/cover.html', context)


def about(request):
    context = RequestContext(request)
    return render_to_response('core/about.html', context)

def help(request):
    context = RequestContext(request)
    return render_to_response('core/help.html', context)

def support(request):
    context = RequestContext(request)
    return render_to_response('core/support.html', context)

def explore(request):
    context = RequestContext(request)
    return render_to_response('core/explore.html', context)
