# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150227_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='city',
            field=models.CharField(default='', max_length=60, verbose_name='\u57ce\u5e02'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersettings',
            name='districtcounty',
            field=models.CharField(default='', max_length=60, verbose_name='\u533a\u53bf'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='province',
            field=models.CharField(default='', max_length=60, verbose_name='\u7701\u4efd'),
            preserve_default=False,
        ),
    ]
