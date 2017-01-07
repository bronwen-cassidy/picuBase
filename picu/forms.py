from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import Patient


class PatientSearchForm(forms.Form):
	first_name = forms.CharField(label='First Name (wildcard* accepted):', max_length=200, required=False)
	second_name = forms.CharField(label='Second Name (wildcard* accepted):', max_length=200, required=False)
	date_of_birth = forms.DateField(label='Date of Birth:', required=False, widget=AdminDateWidget)

	class Meta:
		model = Patient
		fields = ['first_name', 'second_name', 'date_of_birth']
		widgets = {
			'date_of_birth': AdminDateWidget,
		}

	def __init__(self, *args, **kwargs):
		super(PatientSearchForm, self).__init__(*args, **kwargs)