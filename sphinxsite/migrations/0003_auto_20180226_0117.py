# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-26 01:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sphinxsite', '0002_auto_20180225_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteuser',
            name='team',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
