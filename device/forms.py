# -*- coding: UTF-8 -*-

import os
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from device.models import Device

class DeviceCreateForm(ModelForm):
    class Meta:
        model = Device
        exclude = ()

class DeviceUpdateForm(ModelForm):
    class Meta:
        model = Device
        exclude = ()

