from picu.models import Admission, Picu
from collections import OrderedDict


def total_year_admissions(year):
	admissions = list(Admission.objects.filter(picu_admission_date__year = year))

	totals = OrderedDict([('total_admissions', 0), ('total_deaths', 0),('mortality_rate', ''),('expected_deaths', ''),('smr', 0.0)])
	total_admissions = OrderedDict([(1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, []), (10, []), (11, []), (12, [])])
	boys = OrderedDict([(1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, []), (10, []), (11, []), (12, [])])
	girls = OrderedDict([(1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, []), (10, []), (11, []), (12, [])])
	discharges = OrderedDict([(1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, []), (10, []), (11, []), (12, [])])
	ventilations = OrderedDict([(1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, []), (10, []), (11, []), (12, [])])
	deaths = OrderedDict([(1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, []), (10, []), (11, []), (12, [])])
	patient_days = OrderedDict([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0)])

	sum_discharges = 0
	sum_boys = 0
	sum_girls = 0
	sum_ventilated = 0
	sum_deaths = 0
	sum_patient_days = 0

	for admission in admissions:
		total_admissions.setdefault(admission.picu_admission_date.month, []).append(admission)
		patient_days[admission.picu_admission_date.month] += admission.length_of_stay()
		sum_patient_days += admission.length_of_stay()
		if admission.patient.gender is 'M':
			boys.setdefault(admission.picu_admission_date.month, []).append(admission)
			sum_boys += 1
		elif admission.patient.gender is 'F':
			girls.setdefault(admission.picu_admission_date.month, []).append(admission)
			sum_girls += 1
		if admission.discharged_date:
			discharges.setdefault(admission.picu_admission_date.month, []).append(admission)
			sum_discharges += 1
		if admission.mechanical_ventilation:
			ventilations.setdefault(admission.picu_admission_date.month, []).append(admission)
			sum_ventilated += 1
		if admission.mortality != '0':
			deaths.setdefault(admission.picu_admission_date.month, []).append(admission)
			sum_deaths += 1

	totals['total_admissions'] = len(admissions)
	totals['total_deaths'] = sum(int(admission.mortality) > 0 for admission in admissions)
	totals['mortality_rate'] = str((totals['total_deaths'] / totals['total_admissions']) * 100) + '%' if len(admissions) > 0 else 0
	totals['expected_deaths'] = sum(admission.mortality_risk() for admission in admissions)
	# SMR = count the mortality and divide that by the exepected deaths
	totals['smr'] = (totals['total_deaths'] / float(totals['expected_deaths'])) if totals['expected_deaths'] > 0 else 0

	sum_admissions = len(admissions)

	return {'admissions': total_admissions, 'totals': totals, 'boys': boys, 'girls': girls, 'discharges': discharges,
	        'ventialtions': ventilations, 'deaths': deaths, 'total_days': patient_days, 'sum_admissions': sum_admissions,
	        'sum_discharges': sum_discharges, 'sum_boys': sum_boys, 'sum_girls': sum_girls, 'sum_ventilated': sum_ventilated,
	        'sum_deaths': sum_deaths, 'sum_patient_days': sum_patient_days}
