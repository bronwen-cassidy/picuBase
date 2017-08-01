""" file containing all the alaysis function required for the charts """

# needs parameters for various options (but we shall see what emerges)
import math

import numpy

from picu.models import Admission


def full_cusum_llr(year):
	admissions = list(find_latest_admissions(year))

	data = []
	odds = []  # consists of doubling_odds and halving_odds
	smr_data = []  # mortality_risk / observed deaths
	llr_for_doubling_odds = [] #=IF(C4=1,LN(O4/E4),LN((1-O4)/(1-E4)))
	llr_for_halving_odds = [] #=-LN(P4/mortality_risk)*mortality+-LN((1-P4)/(1-mortality_risk))*(1-mortality)  p =0.5*mortality_risk/(1-0.5*mortality_risk)

	y_index = 1
	observed_deaths = 0
	smr_range = []
	smr_y_low = 0
	smr_y_high = 0
	mortality_risk_sum = []

	# zero truncated for 2 odds: =IF(U3+Q4<0,0,IF(U3+Q4=4.6,4.6,IF(U3+Q4>4.6,0,U3+Q4)))
	# zero_truncated for 1/2 odds
	# =IF(_risk_list-1 + risk_=4.6,4.6,IF(S3+Q4>4.6,0,IF(S3+Q4=-4.6,-4.6,IF(S3+Q4<-4.6,0,S3+Q4))))
	for admission in admissions:

		mortality_risk = admission.mortality_risk()
		mortality_risk_sum.append(mortality_risk)

		previous_risk = data[len(data)-1][0] if len(data) > 0 else 0
		previous_half_risk = odds[len(odds)-1][0] if len(odds) > 0 else 0

		previous_doubling_odds = llr_for_doubling_odds[len(llr_for_doubling_odds)-1][0] if len(llr_for_doubling_odds) > 0 else 0
		previous_halving_odds = llr_for_halving_odds[len(llr_for_halving_odds)-1][0] if len(llr_for_halving_odds) > 0 else 0

		mortality = admission.mortality
		if mortality == "1":
			risk_ = math.log((2 * mortality_risk / (1 + mortality_risk)) / mortality_risk)
			observed_deaths += 1
		else:
			risk_ = math.log((1 - (2 * mortality_risk) / (1 + mortality_risk)) / (1 - mortality_risk))

		llr_for_doubling_odds.append(risk_)

		new_risk = risk_
		if previous_risk + risk_ > 4.6:
			new_risk = 0
		elif previous_risk + risk_ == -4.6:
			new_risk = -4.6
		elif previous_risk + risk_ < -4.6:
			new_risk = 0
		else:
			new_risk += previous_risk

		## =IF(T3+R4=4.6,4.6,IF(T3+R4>4.6,0,IF(T3+R4=-4.6,-4.6,IF(T3+R4<-4.6,0,T3+R4))))
		######## half llr risk
		p = 0.5 * mortality_risk / (1 - 0.5 * mortality_risk)
		half_risk = -math.log(p / mortality_risk) * mortality + -math.log((1 - p) / (1 - mortality_risk)) * (1 - mortality)
		llr_for_halving_odds.append(half_risk)

		new_half_risk = half_risk
		if previous_half_risk + half_risk > 4.6:
			new_half_risk = 0
		elif previous_half_risk + half_risk == -4.6:
			new_half_risk = -4.6
		elif previous_half_risk + half_risk < -4.6:
			new_half_risk = 0
		else:
			new_half_risk += previous_half_risk
		llr_for_halving_odds.append(new_half_risk)


		smr_low = 0
		smr_high = 0
		smr = observed_deaths/sum(mortality_risk_sum)
		smr_range.append(smr)

		if smr > 0:
			deviation = numpy.std(smr_range)
			my_norm=1.96*(deviation/(math.sqrt(y_index)))
			smr_low = smr - my_norm
			smr_high = smr + my_norm

		data.append((new_risk, y_index))
		odds.append(([zero_half_odds, zero_two_odds], y_index))
		smr_data.append(([smr, smr_low, smr_high], y_index))

		if smr_high > smr_y_high:
			smr_y_high = smr_high
		if smr_low < smr_y_low:
			smr_y_low = smr_low

		y_index += 1

	results_dictionary = {'half_cusum_llr':odds,'full_cusum_llr':data,'full_cusum_llr_count':y_index,'x_range': range(1,y_index),'smr_y_range': [
		smr_y_low, smr_y_high],
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