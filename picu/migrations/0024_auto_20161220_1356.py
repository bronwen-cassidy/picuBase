# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-20 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picu', '0023_auto_20161216_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='admission_diagnosis',
            field=models.ManyToManyField(default=None, related_name='admission', to='picu.Diagnosis'),
        ),
    ]
