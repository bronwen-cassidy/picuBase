from django.contrib import admin
from django.db import models
from django import forms
from .models import Picu,Patient,Admission,Culture,Diagnosis,SelectionType,SelectionValue


################# INLINES ######################
class AdmissionInline(admin.StackedInline):
	extra = 1
	model = Admission
	
class PatientInline(admin.StackedInline):
	model = Patient
	
######################### ADMINS #################	

class PicuAdmin(admin.ModelAdmin):
	formfield_overrides = { models.ManyToManyField: {'widget': forms.SelectMultiple(attrs={'size':'3'})}, }

class DiagnosisAdmin(admin.ModelAdmin):
	list_display = ('name', 'icd_10_code', 'anzics_code')	
	
class AdmissionAdmin(admin.ModelAdmin):
	
	fieldsets = [
        (None, {'fields': ['picu_admission_date', 'admitted_from', 'hospital_admission_date', 'patient',
						   'admission_diagnosis', 'positive_cultures', 'risk_associated_with_diagnosis']}),
		('Status On Admission', 
			{'fields': ['pupils_fixed', 'elective_admission', 'mechanical_ventilation','base_excess', 'sbp',
						'fraction_inspired_oxygen','partial_oxygen_pressure']}),
		('Recovery Post Procedure (Yes/No)', 
			{'fields': ['bypass_cardiac', 'non_bypass_cardiac', 'non_cardiac_procedure']}),
        ('Discharge Information', 
			{'classes': ['collapse'], 
		     'fields': ['discharge_diagnosis', 'discharged_date', 'discharged_to']})
    ]
	
	#inlines = [DiagnosisInline]
	
	list_display = ('picu_admission_date', 'patient_info', 'current_diagnosis', 'pos_cultures','admission_month','mortality','pupils_fixed',
					'elective_admission', 'hiv', 'mechanical_ventilation', 'base_excess', 'sbp','sys_blood_pressure_squared',
				    'fraction_inspired_oxygen','partial_oxygen_pressure', 'ratio_of_fio2_over_pao2', 'bypass_cardiac',
					'non_bypass_cardiac', 'non_cardiac_procedure','risk_associated_with_diagnosis', 'logit', 'length_of_stay', 'mortality_risk')
					
	list_filter = ['picu_admission_date','risk_associated_with_diagnosis']
	search_fields = ['picu_admission_date', 'risk_associated_with_diagnosis', 'elective_admission']
	
class PatientAdmin(admin.ModelAdmin):

	list_display = ('first_name', 'second_name', 'gender', 'date_of_birth', 'hiv', 'age_in_months')	
	list_filter = ['gender', 'date_of_birth', 'first_name', 'second_name', 'hiv']
	search_fields = ['first_name', 'second_name', 'gender', 'date_of_birth', 'hiv']
	
# Register your models here.
admin.site.register(Picu, PicuAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Admission,AdmissionAdmin)
admin.site.register(Culture)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(SelectionType)
admin.site.register(SelectionValue)