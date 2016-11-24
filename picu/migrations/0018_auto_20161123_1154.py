# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picu', '0017_admission_risk_associated_with_diagnosis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='base_excess',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='admission',
            name='fraction_inspired_oxygen',
            field=models.FloatField(default=0.0),
        ),
    ]
