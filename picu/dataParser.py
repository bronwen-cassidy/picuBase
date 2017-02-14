from picu import formatter
from picu.models import Patient, Diagnosis, Culture, Admission, SelectionType


def create_patient(cells):
	firstname = str(cells[6])
	surname = str(cells[7])
	dob = formatter.format_date(str(cells[8]))
	gender = formatter.format_gender(str(cells[9]))

	patient = Patient.objects.filter(first_name=firstname, second_name=surname, date_of_birth=dob,
	                                 gender=gender).order_by('id')[:1]
	if not patient:
		patient = Patient(first_name=firstname, second_name=surname,
		                  date_of_birth=dob, gender=gender,
		                  hiv=formatter.format_hiv(str(cells[12])))
		patient.save()
	else:
		patient.hiv = formatter.format_hiv(str(cells[12]))
		patient.update()

	return patient


def create_diagnoses(cells):
	diagnoses_list = cells[10].split('#')
	icd10_code = cells[14]
	anszic_code = cells[13]
	risk_category_id = cells[27]
	risk_category = SelectionType.objects.get(id=risk_category_id) if not risk_category_id or risk_category_id is not "0" else None

	result = []

	for i, name in enumerate(diagnoses_list):
		diagnosis = Diagnosis.objects.filter(name__iexact=name).order_by('id')[:1]
		if not diagnosis:
			diagnosis = Diagnosis(name = name, icd_10_code=icd10_code, anszic_code=anszic_code, risk_category=risk_category)
			diagnosis.save()
			result.append(diagnosis)
		else:
			diagnosis[0].icd_10_code = icd10_code
			diagnosis[0].anszic_code = anszic_code
			diagnosis[0].risk_category = risk_category
			diagnosis[0].save()
			result.append(diagnosis[0])
	return result


def create_cultures(cells):
	culture_list = cells[10].split('#')
	result = []

	for i, name in enumerate(culture_list):
		culture = Culture.objects.filter(name__iexact=name).order_by('id')[:1]
		if not culture:
			culture = Culture(name = name)
			culture.save()
			result.append(culture)
		else:
			result.append(culture[0])

	return result


def create_admission(cells):
	patient = create_patient(cells)
	diagnoses_list = list(create_diagnoses(cells))
	postive_cultures_list = list(create_cultures(cells))

	referred_from = cells[3]
	picu_admisison_date = formatter.format_date(cells[4])
	hosp_admission_date = formatter.format_date(cells[5])
	risk = SelectionType.objects.get(id=cells[27]) if cells[27] is not "0" else None
	picu_discharge_date = formatter.format_date(cells[15])
	hospital_discharge_date = formatter.format_date(cells[16])
	discharged_to = cells[17]
	death_in_picu = formatter.format_boolean(cells[18])
	death_in_hospital = formatter.format_boolean(cells[19])
	death_after_discharge = formatter.format_boolean(cells[20])
	pupils_fixed = formatter.format_boolean(cells[21])
	elective_admisison = formatter.format_boolean(cells[22])
	mechanical_ventilation = formatter.format_boolean(cells[23])
	bypass_cardiac = formatter.format_boolean(cells[24])
	non_bypass_cardiac = formatter.format_boolean(cells[25])
	non_cardiac = formatter.format_boolean(cells[26])
	base_excess = cells[29] if cells[29] else "0.0"
	sbp = cells[30] if cells[30] else "0"
	fio2 = cells[31] if cells[31] else "0.0"
	pao2 = cells[32] if cells[32] else "0.0"

	admission = Admission(patient=patient,picu_admission_date=picu_admisison_date, admitted_from=referred_from,
	                      hospital_admission_date=hosp_admission_date, risk_associated_with_diagnosis=risk, pupils_fixed=pupils_fixed,
	                      elective_admission=elective_admisison,mechanical_ventilation=mechanical_ventilation, bypass_cardiac=bypass_cardiac,
	                      non_bypass_cardiac=non_bypass_cardiac,non_cardiac_procedure=non_cardiac, base_excess=base_excess, sbp=sbp,
	                      fraction_inspired_oxygen=fio2,partial_oxygen_pressure=pao2, discharged_date=picu_discharge_date,
	                      discharged_to=discharged_to,death_in_picu=death_in_picu, death_in_hospital=death_in_hospital,
	                      survival_post_icu_discharge=not death_after_discharge, hosp_discharged_date=hospital_discharge_date)

	admission.save()
	admission.admission_diagnosis.add(*diagnoses_list)
	admission.positive_cultures.add(*postive_cultures_list)
	admission.save()
	return admission