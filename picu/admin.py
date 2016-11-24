from django.contrib import admin
from django.db import models
from django import forms
from .models import Picu, Patient, Admission,Culture,PositiveCulture,Diagnosis,AdmissionDiagnosis

class PicuAdmin(admin.ModelAdmin):
	formfield_overrides = { models.ManyToManyField: {'widget': forms.SelectMultiple(attrs={'size':'3'})}, }

class AdmissionInline(admin.StackedInline):
	model = Admission
	
class CultureInline(admin.StackedInline):
	extra = 2
	model = Culture
	
class DiagnosisInline(admin.StackedInline):
	extra = 2
	model = Diagnosis
	
class PatientInline(admin.StackedInline):
	model = Patient

class AdmissionAdmin(admin.ModelAdmin):
	formfield_overrides = { models.ManyToManyField: {'widget': forms.SelectMultiple(attrs={'size':'3'})}, }
	fieldsets = [
        (None, {'fields': ['admission_date', 'admitted_from', 'patient', 'admission_diagnosis','positive_cultures', 
						   'risk_associated_with_diagnosis']}),
		('Status On Admission', 
			{'fields': ['pupils_fixed', 'elective_admission', 'mechanical_ventilation','base_excess', 'sbp',
						'fraction_inspired_oxygen','partial_oxygen_pressure']}),
		('Recovery Post Procedure (Yes/No)', 
			{'fields': ['bypass_cardiac', 'non_bypass_cardiac', 'non_cardiac_procedure']}),
        ('Discharge Information', 
			{'classes': ['collapse'], 
		     'fields': ['discharge_diagnosis', 'discharged_date', 'discharged_to']})
    ]
	list_display = ('admission_date', 'patient_info', 'current_diagnosis', 'pos_cultures','admission_month','mortality','sbp',
				    'sys_blood_pressure_squared','fraction_inspired_oxygen','partial_oxygen_pressure', 'logit')
	
class PatientAdmin(admin.ModelAdmin):

	fieldsets = [
        (None, {'fields': ['first_name', 'second_name', 'gender', 'date_of_birth']})
    ]

	inlines = [AdmissionInline]
	list_display = ('first_name', 'second_name', 'gender', 'date_of_birth', 'age_in_months')
	list_filter = ['gender', 'date_of_birth', 'first_name', 'second_name']
	search_fields = ['first_name', 'second_name', 'gender', 'age_in_months']
	
# Register your models here.
admin.site.register(Picu, PicuAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Admission,AdmissionAdmin)
admin.site.register(Culture)
admin.site.register(PositiveCulture)
admin.site.register(Diagnosis)
admin.site.register(AdmissionDiagnosis)