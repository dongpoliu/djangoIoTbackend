# -*- coding: UTF-8 -*-

import os
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from device.models import Device

class DeviceCreateForm(ModelForm):
    coordinates = forms.CharField(max_length=200, required=True)  
    
    class Meta:
        model = Device
        exclude = ('slug', )
           
    def clean(self):
        cleaned_data = self.cleaned_data

        coordinates = cleaned_data.get("coordinates")
        name = cleaned_data.get("name")
        desc = cleaned_data.get("desc")
        thumbnail = cleaned_data.get("thumbnail")
        return cleaned_data 

class DeviceUpdateForm(ModelForm):
    class Meta:
        model = Device
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(DeviceUpdateForm, self).__init__(*args, **kwargs)

        # Set date and time formats to those supported by the
        # bootstrap-datetimepicker widget.
        self.fields['record_date'].widget.format = DATE_FORMAT
        self.fields['record_time'].widget.format = TIME_FORMAT

        delete_url = reverse('glucose_delete', args=(self.instance.id,))
        self.helper.add_input(Button('delete', 'Delete',
                                     onclick='location.href="%s";' % delete_url,
                                     css_class='btn-danger pull-right'))

