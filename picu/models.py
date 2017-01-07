from django.db import models
from django.utils import timezone
import datetime
from datetime import date
import math
from decimal import Decimal

# Create your models here.


class Picu(models.Model):
	name = models.CharField(max_length=300)
	street_address = models.CharField(max_length=1000)
	city = models.CharField(max_length = 500)
	hospital_number = models.CharField(max_length=200)	
	unit_number = models.CharField(max_length=200)
	case_number = models.CharField(max_length=200)
	
	
	class Meta:
		verbose_name_plural = 'Pediatric ICUS'
	
	def case_number_def(self):
		return self.unit_number + self.case_number
	
	def __str__(self):
		return self.name + " in " + self.city		


class SelectionType(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=400)
	
	def __str__(self):
		return self.name


class SelectionValue(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=400)
	sort_order = models.IntegerField()
	numeric_value = models.CharField(max_length=200, default=None, blank=True, null=True)
	type = models.ForeignKey(SelectionType, on_delete=models.CASCADE)


class Patient(models.Model):
	GENDER_CHOICES = (('M','Male'),('F','Female'))
	STATUS_CHOICES = (('Y','Yes'),('N','No'))
	
	first_name = models.CharField(max_length=300)
	second_name = models.CharField(max_length=300)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None)
	date_of_birth = models.DateField()	
	hiv = models.BooleanField(default=False)
		
	def age_in_months(self):
		today = timezone.now()
		return ((today.year - self.date_of_birth.year) * 12 + today.month - self.date_of_birth.month)
	
	def __str__(self):
		return self.first_name + " " + self.second_name

	age_in_months.short_description = "Age in months"


class Diagnosis(models.Model):	
	name = models.CharField(max_length=500)
	# International Classification of Diseases code
	icd_10_code = models.CharField(max_length=20)
	# Australian and New Zealand Intensive Care diagnostic Code
	anzics_code = models.CharField(max_length=30)
	
	class Meta:
		verbose_name_plural = 'Diagnoses'
		
	def __str__(self):
		return self.name
	

class Culture(models.Model):
	name = models.CharField(max_length=300)
	
	def __str__(self):
		return self.name


class Admission(models.Model):
	LOW_RISK = '1'
	HIGH_RISK = '2'
	VERY_HIGH_RISK = '3'
	DIAGNOSIS_RISK_CHOICES = ((LOW_RISK,'Low Risk'),(HIGH_RISK,'High Risk'),(VERY_HIGH_RISK,'Very High Risk'))
	
	picu_admission_date = models.DateField()
	admitted_from = models.CharField("Referred From", max_length=300)
	hospital_admission_date = models.DateField(default = None)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	admission_diagnosis = models.ManyToManyField(Diagnosis, default=None, related_name="admission")
	risk_associated_with_diagnosis = models.CharField(max_length=1, choices=DIAGNOSIS_RISK_CHOICES, default=None)
	positive_cultures = models.ManyToManyField(Culture, default=None)
	
	pupils_fixed = models.BooleanField("Pupils Fixed To Light?", default=False)
	elective_admission = models.BooleanField(default=False)
	mechanical_ventilation = models.BooleanField("Mechanical ventilation in the first hour?", default=False)
	
	bypass_cardiac = models.BooleanField(default=False)
	non_bypass_cardiac = models.BooleanField("Non-bypass cardiac", default=False)
	non_cardiac_procedure = models.BooleanField(default=False)
	
	base_excess = models.FloatField("Absolute value of base excess (mmol/L)", default=0.0)
	sbp = models.IntegerField("SBP at admission (mm Hg)", default=0)
	fraction_inspired_oxygen = models.FloatField("FiO2 as Decimal", default=0.0)
	partial_oxygen_pressure = models.FloatField("PaO2 mmHg", default=0.0)
	
	discharged_date = models.DateField(default=None, blank=True, null=True)
	discharge_diagnosis = models.TextField(max_length=400, default=None, blank=True, null=True)
	discharged_to = models.CharField(max_length=300, default=None, blank=True, null=True)
	
	def admission_month(self):
		return self.picu_admission_date.month
	
	def length_of_stay(self):
		current_date = self.discharged_date
		if current_date is None:
			current_date = datetime.date.today()
		delta = current_date - self.picu_admission_date		
		return delta.days
		
	def patient_info(self):
		return self.patient
		
	def hiv(self):
		return self.patient.hiv
		
	def age_in_months(self):
		return self.patient.age_in_months()
	
	def current_diagnosis(self):
		return ', '.join([a.name for a in self.admission_diagnosis.all()])
	
	def pos_cultures(self):
		return ', '.join([a.name for a in self.positive_cultures.all()])
		
	def month_discharged(self):
		if self.discharged_date is None:
			return None
		return self.discharged_date.month

	# todo change this into a selection type/value
	def mortality(self):
		return 'Y' if self.discharged_to is not None and self.discharged_to.lower is "death" else 'N'
						
	def sys_blood_pressure_squared(self):
		return (self.sbp * self.sbp) / 1000
	
	def ratio_of_fio2_over_pao2(self):
		return 100 * self.fraction_inspired_oxygen / self.partial_oxygen_pressure if self.partial_oxygen_pressure > 0 and self.fraction_inspired_oxygen > 0  else 0.23
	
	def bool_to_number(self, booleanArg):
		return 1 if booleanArg is True else 0
	
	def calc_diagnostic_risk(self, choice):
		for key,value in self.DIAGNOSIS_RISK_CHOICES:
			if key is choice and key is self.risk_associated_with_diagnosis:
				return 1
		return 0
		
	def logit(self):
		return (self.bool_to_number(self.pupils_fixed) * 3.8233) + (self.bool_to_number(self.elective_admission) * -0.5378) \
		+ (self.bool_to_number(self.mechanical_ventilation) * 0.9763) + (self.base_excess * 0.0671) \
		+ (self.sbp * -0.0431) + (0.1716 * self.sys_blood_pressure_squared()) \
		+ (self.ratio_of_fio2_over_pao2() * 0.4214) + (self.bool_to_number(self.bypass_cardiac) * -1.2246) \
		+ (self.bool_to_number(self.non_bypass_cardiac) * -0.8762) + (self.bool_to_number(self.non_cardiac_procedure) * -1.5164) \
		+ (self.calc_diagnostic_risk(self.VERY_HIGH_RISK) * 1.6225) + (self.calc_diagnostic_risk(self.HIGH_RISK) * 1.0725) \
		+ (self.calc_diagnostic_risk(self.LOW_RISK) * -2.1766) + (-1.7928)
	
	def mortality_risk(self):
		risk_factor = math.exp(self.logit())
		return 0 if not self.age_in_months() > 0 else (risk_factor / (1 + risk_factor)) 
		
	def __str__(self):
		return str(self.patient)
		
	admission_month.admin_order_field = "picu_admission_date"
	admission_month.short_description = "Admission Month"
	length_of_stay.short_description = "LOS"
	patient_info.short_description = "Patient"
	current_diagnosis.short_description = "Diagnosis"
	sys_blood_pressure_squared.short_description = "sbt*sbt/1000"
	ratio_of_fio2_over_pao2.short_description = "100 × Fio2/Pao2 (mm Hg)"
	mortality_risk.short_description="Mortality Risk"
	
	