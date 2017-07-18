""" file containing all the alaysis function required for the charts """

# needs parameters for various options (but we shall see what emerges)
from math import log

from picu.models import Admission


def full_cusum_llr(year):
	# mortality risk > 0 need a given year
	admissions = list(find_latest_admissions(year))
	data = []

	y_index = 1
	x = 0
	# if observed death = 1 (mortality = 1) then log ((2*mortality_risk/(1+mortality_risk))/mortality_risk)
	for admission in admissions:

		#  IF(mortality == 1,LN(O3/E3), LN((1-O3)/(1-E3)))     03=2*E3/(1+E3)
		mortality_risk = admission.mortality_risk()
		if admission.mortality() == "1":
			x = (log((2 * mortality_risk/(1 + mortality_risk)) / mortality_risk))
		else:   # log((1-O3)/(1-E3)    E3=mortality_risk
			x = (log((1 - (2 * mortality_risk / 1 + mortality_risk)) / (1-mortality_risk)))

		data.append((x, y_index))
		y_index += 1

	results_dictionary = {'full_cusum_llr': data, 'full_cusum_llr_count' : y_index}
	return results_dictionary


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


class ChartData(object):

	def __init__(self, data, num_results):
		self.data = data
		self.num_results = num_results