# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picu', '0010_auto_20161119_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='discharge_diagnosis',
            field=models.TextField(blank=True, default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='admission',
            name='discharged_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
