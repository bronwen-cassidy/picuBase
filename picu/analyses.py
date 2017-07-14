""" file containing all the alaysis function required for the charts """

# needs parameters for various options (but we shall see what emerges)
from collections import OrderedDict

from django.db.models import Max

from picu import formatter
from picu.models import Admission, Patient


def full_cusum_llr(year):
	# mortality risk > 0 need a given year
	admissions = list(Admission.objects.filter(picu_admission_date__year=year).order_by('admission_date'))
	admissions_list = []
	yaxis_count = 0
	observed_deaths = 0
	for admission in admissions:
		if admission.mortality_risk() > 0:
			yaxis_count += 1
			admissions_list.append(admission)

	for admission in admissions_list:
		death = formatter.format_boolean(admission.mortality)

	data = [[]]
	return data

""" 
	looking for the patients last admission for the year. This will work for the smr collection as find the first admission
	date of the first patient that died then find all the admission with a date >= to that date. This needs to be the 
	last admisison for each patient
"""
def find_latest_admissions(year):

	admissions = Admission.objects.raw(
		'SELECT distinct(pa.patient_id), pa.* from picu_admission pa where year(pa.picu_admission_date) = ' + str(year) +
		' and pa.picu_admission_date = '
		'(select max(pa2.picu_admission_date) from picu_admission pa2 '
		'where pa.patient_id = pa2.patient_id)')

	return admissions