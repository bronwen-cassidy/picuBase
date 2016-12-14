# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picu', '0004_culture_positiveculture'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmissionDiagnosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='admission',
            name='admission_diagnosis',
        ),
        migrations.AddField(
            model_name='admissiondiagnosis',
            name='admission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picu.Admission'),
        ),
        migrations.AddField(
            model_name='admissiondiagnosis',
            name='diagnosis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picu.Diagnosis'),
        ),
    ]