from django.db import models
from django.utils import timezone
import datetime
from decimal import Decimal

# Create your models here.

class Picu(models.Model):
	name = models.CharField(max_length=300)
	street_address = models.CharField(max_length=1000)
	city = models.CharField(max_length = 500)
	
	class Meta:
		verbose_name_plural = 'Pediatric ICUS'
	
	def __str__(self):
		return self.name + " in " + self.city		

class SelectionType(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=400)
	
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
	date_deceased = models.DateField(default=None, blank=True, null=True)	
	hiv = models.BooleanField(default=False)
		
	def age_in_months(self):
		today = timezone.now()
		return ((today.year - self.date_of_birth.year) * 12 + today.month - self.date_of_birth.month)	

	def hiv_default():
		return false
	
	def __str__(self):
		return self.first_name + " " + self.second_name

	age_in_months.short_description = "Age in months"
	
class Diagnosis(models.Model):	
	name = models.CharField(max_length=500)
	
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
	
	admission_date = models.DateField()
	admitted_from = models.CharField(max_length=300)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	admission_diagnosis = models.ManyToManyField(Diagnosis, default=None)
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
		return self.admission_date.month
	
	def length_of_stay(self):
		current_date = self.discharged_date
		if current_date is None:
			current_date = timezone.now()
		return datetime.strptime(current_date) - datetime.strptime(self.admission_date)
		
	def patient_info(self):
		return self.patient
	
	def current_diagnosis(self):
		return ', '.join([a.name for a in self.admission_diagnosis.all()])
	
	def pos_cultures(self):
		return ', '.join([a.name for a in self.positive_cultures.all()])
		
	def month_discharged(self):
		if self.discharged_date is None:
			return None
		return self.discharged_date.month
	
	def mortality(self):
		return 'Y' if self.discharged_to is not None or self.discharged_to.lower is "death" else 'N'
						
	def sys_blood_pressure_squared(self):
		return (self.sbp * self.sbp) / 1000
	
	def ratio_of_fio2_over_pao2(self):
		return 100 * self.fraction_inspired_oxygen / self.partial_oxygen_pressure if self.partial_oxygen_pressure > 0 and self.fraction_inspired_oxygen > 0  else 0.23
	
	def boolNumConversion(self, booleanArg):
		return 1 if booleanArg is True else 0
	
	def calcDiagnosicRisk(self, choice):
		result = [1 for key, value in DIAGNOSIS_RISK_CHOICES if key is choice and key is self.risk_associated_with_diagnosis]
		return 0 if result is None else 1  
	
	def logit(self):
		return (self.boolNumConversion(self.pupils_fixed) * 3.8233) + (self.boolNumConversion(self.elective_admission) * -0.5378) \
		+ (self.boolNumConversion(self.mechanical_ventilation) * 0.9763) + (self.base_excess * 0.0671) \
		+ (self.sys_blood_pressure_squared() * -0.0431) + ((0.1761 * self.sys_blood_pressure_squared() * self.sys_blood_pressure_squared()) / 1000.0) \
		+ (self.fraction_inspired_oxygen * 0.4214) + (self.boolNumConversion(self.bypass_cardiac) * -1.2246) \
		+ (self.boolNumConversion(self.non_bypass_cardiac) * -0.8762) + (self.boolNumConversion(self.non_cardiac_procedure) * -1.5164) \
		+ (self.calcDiagnosicRisk(self.VERY_HIGH_RISK) * 1.6225) + (self.calcDiagnosicRisk(self.HIGH_RISK) * 1.0725) \
		+ (self.calcDiagnosicRisk(self.LOW_RISK) * -2.1766) - 1.7928

		
	def __str__(self):
		return str(self.patient)
		
	admission_month.admin_order_field = "admission_date"
	admission_month.short_description = "Admission Month"
	length_of_stay.admin_order_field = "length_of_stay"
	length_of_stay.short_description = "Days"
	patient_info.admin_order_field = "patient_info"
	patient_info.short_description = "Patient"
	current_diagnosis.admin_order_field = "current_diagnosis"
	current_diagnosis.short_description = "Diagnosis"
	sys_blood_pressure_squared.short_description = "sbt*sbt/1000"
	ratio_of_fio2_over_pao2.short_description = "100 × Fio2/Pao2 (mm Hg)"
	
class AdmissionDiagnosis(models.Model):
	admission = models.ForeignKey(Admission)
	diagnosis = models.ForeignKey(Diagnosis)
		
class PositiveCulture(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	culture = models.ForeignKey(Culture, on_delete=models.CASCADE)	
	
		
	
	
	
	