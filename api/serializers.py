# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from device.models import Device
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
