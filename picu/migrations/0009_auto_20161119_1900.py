# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picu', '0008_auto_20161119_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_deceased',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
