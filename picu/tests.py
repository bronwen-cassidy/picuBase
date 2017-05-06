import os

from django.test import TestCase

from datetime import date, datetime
from django.core.urlresolvers import reverse

from picu import formatter, summaries
from picu.models import Admission, Patient
from picu.forms import PatientSearchForm

def create_addmission(addmission_date, patient, risk, pos_cultures, pupils_fixed, ventilation, bypass_cardiac, base_excess, sbp, fio):
	return Admission.objects.create(picu_admission_date=addmission_date, admitted_from='Test', hospital_admission_date=addmission_date,
									patient=patient, risk_associated_with_diagnosis=risk, positive_cultures=pos_cultures, pupils_fixed=pupils_fixed,
									mechanical_ventilation=ventilation, bypass_cardiac=bypass_cardiac, non_bypass_cardiac=not bypass_cardiac,
									non_cardiac_procedure=not bypass_cardiac, base_excess=base_excess, sbp=sbp, fraction_inspired_oxygen=fio)


def create_patient(first_name, second_name, dob, hiv, gender):
	return Patient.objects.create(first_name=first_name, second_name=second_name, date_of_birth=dob, hiv=hiv, gender=gender)

class GenericMethodTests(TestCase):

	def test_parse_date(self):
		result = formatter.format_date("12-Feb-15")
		self.assertEquals("2015-02-12", str(result))

	def test_format_hiv(self):
		expected = "0"
		actual = formatter.format_hiv("Unknown")
		self.assertEquals(expected, actual)

	def test_format_hiv_no_val(self):
		actual = formatter.format_hiv("r")
		self.assertEquals("0", actual)

class SummariesTest(TestCase):
	fixtures = ['selection_types', 'selection_values', 'test_summary_reports']

	def test_total_year_admissions(self):

		admission_dictionary = summaries.total_year_admissions(year="2016")

		self.assertEquals(12, len(admission_dictionary['admissions']))

		# get the list for june and assert we have 2 entries
		list_values = admission_dictionary['admissions'].get(5)
		self.assertEquals(2, len(list_values))

	def test_total_deaths(self):

		admission_dictionary = summaries.total_year_admissions(year="2016")

		# get the list for june and assert we have 2 entries
		total_deaths = admission_dictionary['totals'].get('total_deaths')
		self.assertEquals(4, total_deaths)

	def test_total_admissions(self):

		admission_dictionary = summaries.total_year_admissions(year="2016")

		# get the list for june and assert we have 2 entries
		total_admissions = admission_dictionary['totals'].get('total_admissions')
		self.assertEquals(5, total_admissions)

	def test_mortality_rate(self):

		admission_dictionary = summaries.total_year_admissions(year="2016")

		# get the list for june and assert we have 2 entries
		mortality_rate = admission_dictionary['totals'].get('mortality_rate')
		self.assertEquals('80.0%', mortality_rate)

	def test_expected_deaths(self):

		admission_dictionary = summaries.total_year_admissions(year="2016")

		# get the list for june and assert we have 2 entries
		expected_deaths = admission_dictionary['totals'].get('expected_deaths')
		self.assertEquals('0.46501316724104913', expected_deaths)

	def test_smr(self):

		admission_dictionary = summaries.total_year_admissions(year="2016")

		# get the list for june and assert we have 2 entries
		smr = admission_dictionary['totals'].get('smr')
		self.assertEquals(8.601906960467891, smr)


# Create your tests here.
class AdmissionMethodTests(TestCase):


	def test_admission_month(self):
		#admin_date = date('2016-01-01') #date(year=2016, month=4, day=12)
		admin_date = datetime.strptime("2016-04-01", "%Y-%m-%d")
		my_admission = Admission()
		my_admission.picu_admission_date = admin_date
		self.assertEqual(4, my_admission.admission_month())


# not yet class AdmissionViewTests(TestCase):


class PatientViewTests(TestCase):
	def test_index_no_search(self):
		response = self.client.get(reverse('picu:home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No patients available")
		self.assertContains(response, "First Name (wildcard* accepted):")
		self.assertIsInstance(response.context['form'], PatientSearchForm)
		self.assertQuerysetEqual([], response.context['patient_list'])

	def test_form_renders_dob_field(self):
		form = PatientSearchForm()
		self.assertIn('date_of_birth', form.as_p())

	# self.fail(form.as_p())

	def test_patient_search_first_name_like(self):
		# create a couple of patients
		create_patient(first_name='Fred', second_name='Benny', dob=date(year=2016, month=10, day=12), hiv=False, gender='M')
		create_patient(first_name='Fredie', second_name='Sam', dob=date(year=2015, month=1, day=22), hiv=False, gender='M')
		create_patient(first_name='Fredamina', second_name='Alice', dob=date(year=2016, month=5, day=7), hiv=False, gender='F')
		form_data = {'first_name': 'Fred', 'second_name': '', 'dob': ''}

		response = self.client.post(reverse('picu:patient_search'), data=form_data)
		self.assertEqual(response.status_code, 200)
		patient_list_ = response.context['patient_list']
		self.assertEqual(3, len(patient_list_))

	def test_patient_search_second_and_first_name_like(self):
		# create a couple of patients
		create_patient(first_name='Fred', second_name='Benny', dob=date(year=2016, month=10, day=12), hiv=False, gender='M')
		create_patient(first_name='Fredie', second_name='Sam', dob=date(year=2015, month=1, day=22), hiv=False, gender='M')
		create_patient(first_name='Fredamina', second_name='Alice', dob=date(year=2016, month=5, day=7), hiv=False, gender='F')
		form_data = {'first_name': 'Fred', 'second_name': 'Benny', 'dob': ''}

		response = self.client.post(reverse('picu:patient_search'), data=form_data)
		self.assertEqual(response.status_code, 200)
		patient_list_ = response.context['patient_list']
		self.assertEqual(1, len(patient_list_))

	def test_patient_search_dob_eq(self):
		# create a couple of patients
		create_patient(first_name='Fred', second_name='Benny', dob=date(year=2016, month=10, day=12), hiv=False, gender='M')
		create_patient(first_name='Fredie', second_name='Sam', dob=date(year=2015, month=1, day=22), hiv=False, gender='M')
		create_patient(first_name='Fredamina', second_name='Alice', dob=date(year=2016, month=5, day=7), hiv=False, gender='F')
		form_data = {'first_name': 'Fred', 'second_name': 'e', 'date_of_birth': '2016-05-07'}

		response = self.client.post(reverse('picu:patient_search'), data=form_data)
		self.assertEqual(response.status_code, 200)
		patient_list_ = response.context['patient_list']
		self.assertEqual(1, len(patient_list_))
		self.assertEqual('Alice', patient_list_[0].second_name)


class DataUploadViewTests(TestCase):

	fixtures = ['selection_types', 'selection_values']

	def test_data_import(self):

		with open(os.path.join(os.path.dirname(__file__)) + '/test_data/data.csv', 'r') as file_data:
			response = self.client.post(reverse('picu:data_import'), {'datafile': file_data})
			self.assertEqual(response.status_code, 200)

		# lets go and find some of that information
		patient = Patient.objects.filter(first_name = 'a111', second_name='b111')[0]
		self.assertEqual('31-May-16', patient.date_of_birth.strftime('%d-%b-%y'))
		admission = Admission.objects.filter(picu_admission_date=formatter.format_date('19-Jun-16'), admitted_from='Sasolburg')
		self.assertEqual(1, len(admission))
