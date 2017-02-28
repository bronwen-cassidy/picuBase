# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 12:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picu_admission_date', models.DateField()),
                ('admitted_from', models.CharField(max_length=300, verbose_name='Referred From')),
                ('hospital_admission_date', models.DateField(default=None)),
                ('pupils_fixed', models.BooleanField(default=False, verbose_name='Pupils Fixed To Light?')),
                ('elective_admission', models.BooleanField(default=False)),
                ('mechanical_ventilation', models.BooleanField(default=False, verbose_name='Mechanical ventilation in the first hour?')),
                ('bypass_cardiac', models.BooleanField(default=False)),
                ('non_bypass_cardiac', models.BooleanField(default=False, verbose_name='Non-bypass cardiac')),
                ('non_cardiac_procedure', models.BooleanField(default=False)),
                ('base_excess', models.FloatField(default=0.0, verbose_name='Absolute value of base excess (mmol/L)')),
                ('sbp', models.IntegerField(default=0, verbose_name='SBP at admission (mm Hg)')),
                ('fraction_inspired_oxygen', models.FloatField(default=0.0, verbose_name='FiO2 as Decimal')),
                ('partial_oxygen_pressure', models.FloatField(default=0.0, verbose_name='PaO2 KPa')),
                ('discharged_date', models.DateField(blank=True, default=None, null=True)),
                ('hosp_discharged_date', models.DateField(blank=True, default=None, null=True)),
                ('discharge_diagnosis', models.TextField(blank=True, default=None, max_length=400, null=True)),
                ('discharged_to', models.TextField(blank=True, default=None, max_length=4000, null=True)),
                ('death_in_picu', models.BooleanField(default=False)),
                ('death_in_hospital', models.BooleanField(default=False)),
                ('survival_post_icu_discharge', models.BooleanField(default=False)),
                ('case_no', models.CharField(default='1', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('icd_10_code', models.CharField(default=None, max_length=20)),
                ('anszic_code', models.CharField(default=None, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Diagnoses',
            },
        ),
        migrations.CreateModel(
            name='DiagnosticCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=4000)),
                ('short_description', models.CharField(max_length=4000)),
                ('icd10_code', models.CharField(default=None, max_length=20, null=True)),
                ('anszic_code', models.CharField(default=None, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=300)),
                ('second_name', models.CharField(max_length=300)),
                ('hospital_no', models.CharField(max_length=300)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default=None, max_length=1)),
                ('date_of_birth', models.DateField()),
                ('hiv', models.CharField(choices=[('0', 'Unknown'), ('1', 'Positive'), ('2', 'Negative'), ('3', 'Pending')], default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Picu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('street_address', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=500)),
                ('unit_number', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Pediatric ICUS',
            },
        ),
        migrations.CreateModel(
            name='SelectionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='SelectionValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=400)),
                ('sort_order', models.IntegerField()),
                ('numeric_value', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picu.SelectionType')),
            ],
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='risk_category',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='picu.SelectionType'),
        ),
        migrations.AddField(
            model_name='admission',
            name='admission_diagnosis',
            field=models.ManyToManyField(default=None, related_name='admission', to='picu.Diagnosis'),
        ),
        migrations.AddField(
            model_name='admission',
            name='condition_associated_with_risk',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='risk_condition', to='picu.Diagnosis'),
        ),
        migrations.AddField(
            model_name='admission',
            name='main_admission_reason',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='picu.SelectionValue'),
        ),
        migrations.AddField(
            model_name='admission',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picu.Patient'),
        ),
        migrations.AddField(
            model_name='admission',
            name='picu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picu.Picu'),
        ),
        migrations.AddField(
            model_name='admission',
            name='positive_cultures',
            field=models.ManyToManyField(default=None, to='picu.Culture'),
        ),
        migrations.AddField(
            model_name='admission',
            name='risk_associated_with_diagnosis',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='picu.SelectionType'),
        ),
    ]
