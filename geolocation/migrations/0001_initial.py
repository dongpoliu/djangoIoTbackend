# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('plain_location', location_field.models.plain.PlainLocationField(max_length=63)),
                ('lon', models.FloatField(null=True)),
                ('lat', models.FloatField(null=True)),
            ],
            options={
                'ordering': ['city'],
            },
            bases=(models.Model,),
        ),
    ]
