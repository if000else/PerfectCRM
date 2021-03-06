# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-10 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20180607_2032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name_plural': '视图菜单'},
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '已报名'), (1, '未报名'), (2, '已退学')], default=1),
        ),
    ]
