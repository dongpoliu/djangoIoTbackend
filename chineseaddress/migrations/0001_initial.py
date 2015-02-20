# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=165, verbose_name='\u540d\u79f0', blank=True)),
                ('street_number', models.CharField(max_length=20, verbose_name='\u8be6\u7ec6\u5730\u5740', blank=True)),
                ('route', models.CharField(max_length=100, verbose_name='\u8def\u7ebf', blank=True)),
                ('latitude', models.FloatField(null=True, verbose_name='\u7eac\u5ea6', blank=True)),
                ('longitude', models.FloatField(null=True, verbose_name='\u7ecf\u5ea6', blank=True)),
            ],
            options={
                'ordering': ('villagetown', 'route', 'street_number'),
                'verbose_name_plural': '\u5730\u5740',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=165, verbose_name='\u57ce\u5e02', blank=True)),
            ],
            options={
                'ordering': ('province', 'name'),
                'verbose_name_plural': '\u57ce\u5e02',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40, verbose_name='\u56fd\u5bb6', blank=True)),
                ('code', models.CharField(max_length=2, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': '\u56fd\u5bb6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DistrictCounty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=165, verbose_name='\u533a\u53bf', blank=True)),
                ('city', models.ForeignKey(related_name='districtcounties', to='chineseaddress.City')),
            ],
            options={
                'ordering': ('city', 'name'),
                'verbose_name_plural': '\u533a\u53bf',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=165, verbose_name='\u7701\u4efd', blank=True)),
                ('country', models.ForeignKey(related_name='provinces', to='chineseaddress.Country')),
            ],
            options={
                'ordering': ('country', 'name'),
                'verbose_name_plural': '\u7701\u4efd',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VillageTown',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=165, verbose_name='\u8857\u9053\u4e61\u9547', blank=True)),
                ('postal_code', models.CharField(max_length=10, verbose_name='\u90ae\u7f16', blank=True)),
                ('districtcounty', models.ForeignKey(related_name='villagetowns', to='chineseaddress.DistrictCounty')),
            ],
            options={
                'ordering': ('districtcounty', 'name'),
                'verbose_name_plural': '\u8857\u9053\u4e61\u9547',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='villagetown',
            unique_together=set([('name', 'districtcounty')]),
        ),
        migrations.AlterUniqueTogether(
            name='province',
            unique_together=set([('name', 'country')]),
        ),
        migrations.AlterUniqueTogether(
            name='districtcounty',
            unique_together=set([('name', 'city')]),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(related_name='cities', to='chineseaddress.Province'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('name', 'province')]),
        ),
        migrations.AddField(
            model_name='address',
            name='villagetown',
            field=models.ForeignKey(related_name='addresses', blank=True, to='chineseaddress.VillageTown', null=True),
            preserve_default=True,
        ),
    ]
