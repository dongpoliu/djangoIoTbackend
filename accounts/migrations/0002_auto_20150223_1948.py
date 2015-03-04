# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='address',
            field=models.CharField(max_length=60, verbose_name='\u5730\u5740'),
            preserve_default=True,
        ),
    ]
