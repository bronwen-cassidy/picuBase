""" file containing all the alaysis function required for the charts """

# needs parameters for various options (but we shall see what emerges)
import math
import numpy
import scipy
from scipy.stats import norm

from picu.models import Admission


def full_cusum_llr(year):
	# mortality risk > 0 need a given year
	admissions = list(find_latest_admissions(year))
	data = []
	smr_data = []  # mortality_risk / observed deaths

	y_index = 1
	observed_deaths = 0
	smr_range = []
	smr_y_low = 0
	smr_y_high = 0
	mortality_risk_sum = []
	x = 0
	# if observed death = 1 (mortality = 1) then log ((2*mortality_risk/(1+mortality_risk))/mortality_risk)
	for admission in admissions:

		#  IF(mortality == 1,LN(O3/E3), LN((1-O3)/(1-E3)))     03=2*E3/(1+E3)
		mortality_risk = admission.mortality_risk()
		mortality_risk_sum.append(mortality_risk)

		if admission.mortality == "1":
			risk_ = (2 * mortality_risk / (1 + mortality_risk)) / mortality_risk
			observed_deaths += 1

		else:   # log((1-O3)/(1-E3)    E3=mortality_risk
			risk_ = (1 - (2 * mortality_risk) / (1 + mortality_risk)) / (1 - mortality_risk)

		smr_low = 0
		smr_high = 0
		smr = observed_deaths/sum(mortality_risk_sum)
		smr_range.append(smr)

		if smr > 0:
			deviation = numpy.std(smr_range)
			#my_norm = scipy.stats.norm.interval(0.05, deviation)
			my_norm=1.96*(deviation/(math.sqrt(y_index)))
			#print(">>>>> " + str(my_norm))
			# returns both + and - norm[1] is the positive
			smr_low = smr - my_norm
			smr_high = smr + my_norm

		x = (math.log(risk_))

		data.append((x, y_index))
		smr_data.append(([smr, smr_low, smr_high], y_index))

		if smr_high > smr_y_high:
			smr_y_high = smr_high
		if smr_low < smr_y_low:
			smr_y_low = smr_low

		y_index += 1

	results_dictionary = {'full_cusum_llr':data,'full_cusum_llr_count':y_index,'x_range': range(1,y_index),'smr_y_range': [smr_y_low, smr_y_high],
	                      'smr':smr_data}
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