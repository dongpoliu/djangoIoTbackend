# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150226_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='airdetectordata_high',
            field=models.PositiveIntegerField(default=99),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='airdetectordata_low',
            field=models.PositiveIntegerField(default=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='airdetectordata_target_max',
            field=models.PositiveIntegerField(default=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='airdetectordata_target_min',
            field=models.PositiveIntegerField(default=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='province',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='\u7701\u4efd', choices=[('\u4eac', '\u5317\u4eac\u5e02'), ('\u6caa', '\u4e0a\u6d77\u5e02'), ('\u6d25', '\u5929\u6d25\u5e02'), ('\u5180', '\u6cb3\u5317\u7701'), ('\u9c81', '\u5c71\u4e1c\u7701'), ('\u8c6b', '\u6cb3\u5357\u7701'), ('\u8fbd', '\u8fbd\u5b81\u7701'), ('\u9ed1', '\u9ed1\u9f99\u6c5f\u7701'), ('\u5409', '\u5409\u6797\u7701'), ('\u8499', '\u5185\u8499\u53e4\u81ea\u6cbb\u533a'), ('\u664b', '\u5c71\u897f\u7701'), ('\u5b81', '\u5b81\u590f\u81ea\u6cbb\u533a'), ('\u9655', '\u9655\u897f\u7701'), ('\u7696', '\u5b89\u5fbd\u7701'), ('\u82cf', '\u6c5f\u82cf\u7701'), ('\u6d59', '\u6d59\u6c5f\u7701'), ('\u8d63', '\u6c5f\u897f\u7701'), ('\u95fd', '\u798f\u5efa\u7701'), ('\u7ca4', '\u5e7f\u4e1c\u7701'), ('\u6842', '\u5e7f\u897f\u7701'), ('\u5ddd', '\u56db\u5ddd\u7701'), ('\u7518', '\u7518\u8083\u7701'), ('\u9752', '\u9752\u6d77\u7701'), ('\u65b0', '\u65b0\u7586\u81ea\u6cbb\u533a'), ('\u85cf', '\u897f\u85cf\u81ea\u6cbb\u533a'), ('\u6fb3', '\u6fb3\u95e8\u7279\u533a'), ('\u6e2f', '\u9999\u6e2f\u7279\u533a'), ('\u6e58', '\u6e56\u5357\u7701'), ('\u9102', '\u6e56\u5317\u7701'), ('\u6ec7', '\u4e91\u5357\u7701'), ('\u8d35', '\u8d35\u5dde\u7701'), ('\u53f0', '\u53f0\u6e7e\u7701'), ('\u6e1d', '\u91cd\u5e86\u5e02')]),
            preserve_default=True,
        ),
    ]
