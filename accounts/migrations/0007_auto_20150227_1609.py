# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150227_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='city',
            field=models.ForeignKey(to='chineseaddress.City'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='districtcounty',
            field=models.ForeignKey(to='chineseaddress.DistrictCounty'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='province',
            field=models.ForeignKey(to='chineseaddress.Province'),
            preserve_default=True,
        ),
    ]
