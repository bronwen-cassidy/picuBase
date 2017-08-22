""" file containing all the alaysis function required for the charts """

# needs parameters for various options (but we shall see what emerges)
import math

import numpy

from picu.models import Admission


def full_cusum_llr(year):
	admissions = list(find_latest_admissions(year))

	smr_data = []  # mortality_risk / observed deaths

	full_cusumllr_2_odds = []
	zero_cusumllr_2_odds = []
	full_cusumllr_half_odds = []
	zero_cusumllr_half_odds = []
	oe_y_min_range = 0
	oe_y_max_range = 0


	cussum_oe_deaths = []
	deaths = []

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

		previous_doubling_odds = zero_cusumllr_2_odds[len(zero_cusumllr_2_odds)-1][0] if len(zero_cusumllr_2_odds) > 0 else 0
		previous_halving_odds = zero_cusumllr_half_odds[len(zero_cusumllr_half_odds)-1][0] if len(zero_cusumllr_half_odds) > 0 else 0
		previous_oe_cussum = cussum_oe_deaths[len(cussum_oe_deaths)-1][0] if len(cussum_oe_deaths) > 0 else 0

##  = -LN(P3/E3)*C3+-LN((1-P3)/(1-E3))*(1-C3)  p = =0.5*E3/(1-0.5*E3)
		mortality = admission.mortality
		if mortality == "1":
			risk_ = math.log((2 * mortality_risk / (1 + mortality_risk)) / mortality_risk)
			observed_deaths += 1
		else:
			risk_ = math.log((1 - (2 * mortality_risk) / (1 + mortality_risk)) / (1 - mortality_risk))
#
		oe_deaths = (previous_oe_cussum + (int(mortality) - mortality_risk))
		cussum_oe_deaths.append((oe_deaths, y_index))
		oe_y_min_range = math.floor(oe_deaths) if math.floor(oe_deaths) < oe_y_min_range else oe_y_min_range
		oe_y_max_range = math.ceil(oe_deaths) if math.ceil(oe_deaths) > oe_y_max_range else oe_y_max_range
		deaths.append((int(mortality), y_index))

		new_risk = risk_
		if previous_doubling_odds + risk_ > 4.6:
			new_risk = 0
		elif previous_doubling_odds + risk_ == -4.6:
			new_risk = -4.6
		elif previous_doubling_odds + risk_ < -4.6:
			new_risk = 0
		else:
			new_risk += previous_doubling_odds

		full_cusumllr_2_odds.append((new_risk, y_index))

		## zero truncated 2 odds: =IF(previous_doubling_odds+Q4<0,0,IF(U3+Q4=4.6,4.6,IF(U3+Q4>4.6,0,U3+Q4)))
		new_zero_risk = risk_
		if previous_doubling_odds + risk_ > 4.6:
			new_zero_risk = 0
		elif previous_doubling_odds + risk_ < 0:
			new_zero_risk = 0
		else:
			new_zero_risk += previous_doubling_odds

		zero_cusumllr_2_odds.append((new_zero_risk, y_index))

		## =IF(T3+R4=4.6,4.6,IF(T3+R4>4.6,0,IF(T3+R4=-4.6,-4.6,IF(T3+R4<-4.6,0,T3+R4))))
		######## half llr risk
		p = 0.5 * mortality_risk / (1 - 0.5 * mortality_risk)
		half_risk = -math.log(p / mortality_risk) * int(mortality) + -math.log((1 - p) / (1 - mortality_risk)) * (1 - int(mortality))

		new_half_risk = half_risk
		if previous_halving_odds + half_risk > 4.6:
			new_half_risk = 0
		elif previous_halving_odds + half_risk == -4.6:
			new_half_risk = -4.6
		elif previous_halving_odds + half_risk < -4.6:
			new_half_risk = 0
		else:
			new_half_risk += previous_halving_odds

		full_cusumllr_half_odds.append((new_half_risk, y_index))

		## zero truncated half risk =IF(V3+R4>0,0,IF(V3+R4=-4.6,-4.6,IF(V3+R4<-4.6,0,V3+R4)))
		new_zero_half_risk = half_risk
		if previous_halving_odds + half_risk > 0:
			new_zero_half_risk = 0
		elif previous_halving_odds + half_risk == -4.6:
			new_zero_half_risk = -4.6
		elif previous_halving_odds + half_risk < -4.6:
			new_zero_half_risk = 0
		else:
			new_zero_half_risk += previous_halving_odds

		zero_cusumllr_half_odds.append((new_zero_half_risk, y_index))

		smr_low = 0
		smr_high = 0
		smr = observed_deaths/sum(mortality_risk_sum)
		smr_range.append(smr)

		if smr > 0:
			deviation = numpy.std(smr_range)
			my_norm=1.96*(deviation/(math.sqrt(y_index)))
			smr_low = smr - my_norm
			smr_high = smr + my_norm

		smr_data.append(([smr, smr_low, smr_high], y_index))

		if smr_high > smr_y_high:
			smr_y_high = smr_high
		if smr_low < smr_y_low:
			smr_y_low = smr_low

		y_index += 1

	results_dictionary = {'oe_y_max_range': oe_y_max_range,'oe_y_min_range': oe_y_min_range, 'deaths': deaths, 'oe_deaths': cussum_oe_deaths,
	                      'zero_half_cusum_llr':zero_cusumllr_half_odds,
	                       'zero_full_cusum_llr':zero_cusumllr_2_odds,
	                      'full_cusum_llr':full_cusumllr_2_odds,'full_cusum_llr_count':y_index,'x_range': range(1,y_index),'smr_y_range': [smr_y_low, smr_y_high], 'smr':smr_data}

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