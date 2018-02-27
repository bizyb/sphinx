# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-27 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sphinxsite', '0005_siteuser_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='invite_code_input',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='team',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
