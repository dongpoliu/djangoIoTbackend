# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime

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
