from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Picu(models.Model):
	name = models.CharField(max_length=300)
	street_address = models.CharField(max_length=1000)
	city = models.CharField(max_length = 500)
	
	def __str__(self):
		return self.name + " in " + self.city
	
class Child(models.Model):
	first_name = models.CharField(max_length=300)
	second_name = models.CharField(max_length=300)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=1)
	
	def get_age_in_months(self):
		today = timezone.now()
		return ((today.year - self.date_of_birth.year) *12 + today.month - self.date_of_birth.month)		
	
	def __str__(self):
		return self.first_name + " " + self.second_name + " " + self.get_age_in_months()		
	
	