# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolocation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=60)),
                ('desc', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=200)),
                ('idsn', models.TextField(max_length=1000)),
                ('ele', models.TextField(max_length=1000)),
                ('private', models.BooleanField(default=True)),
                ('route_to', models.TextField(max_length=1000)),
                ('activate_code', models.TextField(max_length=1000)),
                ('other', models.TextField(max_length=1000)),
                ('slug', models.SlugField(max_length=255)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('online', models.BooleanField(default=True)),
                ('location', models.ForeignKey(to='geolocation.Location')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Device',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='device',
            name='tags',
            field=models.ManyToManyField(to='device.Tag'),
            preserve_default=True,
        ),
    ]
