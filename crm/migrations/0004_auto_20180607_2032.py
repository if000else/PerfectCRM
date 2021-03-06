# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-07 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20180607_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='url_type',
            field=models.SmallIntegerField(choices=[(0, 'relative_name'), (1, 'absolute_url')], default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='url_name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
