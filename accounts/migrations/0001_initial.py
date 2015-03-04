# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chineseaddress', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('air', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('time_zone', timezone_field.fields.TimeZoneField(default=b'Asia/Shanghai')),
                ('airdetectordata_low', models.PositiveIntegerField(default=60)),
                ('airdetectordata_high', models.PositiveIntegerField(default=180)),
                ('airdetectordata_target_min', models.PositiveIntegerField(default=70)),
                ('airdetectordata_target_max', models.PositiveIntegerField(default=120)),
                ('address', models.ForeignKey(verbose_name='\u5730\u5740', to='chineseaddress.Address')),
                ('airdetectordata_unit', models.ForeignKey(default=1, to='air.Unit')),
                ('default_category', models.ForeignKey(to='air.Category', null=True)),
                ('user', models.OneToOneField(related_name='settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '\u7528\u6237\u8bbe\u5b9a',
            },
            bases=(models.Model,),
        ),
    ]
