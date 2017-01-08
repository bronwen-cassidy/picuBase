from django.test import TestCase

from datetime import date
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from picu.models import Admission, Patient
from picu.forms import PatientSearchForm


def create_addmission(addmission_date, patient, risk, pos_cultures, pupils_fixed, ventilation, bypass_cardiac, base_excess, sbp, fio):
	return Admission.objects.create(picu_admission_date=addmission_date, admitted_from='Test', hospital_admission_date=addmission_date,
									patient=patient, risk_associated_with_diagnosis=risk, positive_cultures=pos_cultures, pupils_fixed=pupils_fixed,
									mechanical_ventilation=ventilation, bypass_cardiac=bypass_cardiac, non_bypass_cardiac=not bypass_cardiac,
									non_cardiac_procedure=not bypass_cardiac, base_excess=base_excess, sbp=sbp, fraction_inspired_oxygen=fio)


def create_patient(first_name, second_name, dob, hiv, gender):
	return Patient.objects.create(first_name=first_name, second_name=second_name, date_of_birth=dob, hiv=hiv, gender=gender)


def generate_file(self):
	try:
		myfile = open('test.csv', 'wb')
	# wr = csv.writer(myfile)
	# wr.writerow(('Paper ID', 'Paper Title', 'Authors'))
	# wr.writerow(('1', 'Title1', 'Author1'))
	# wr.writerow(('2', 'Title2', 'Author2'))
	# wr.writerow(('3', 'Title3', 'Author3'))
	finally:
		myfile.close()

	return myfile


# Create your tests here.
class AdmissionMethodTests(TestCase):
	def test_admission_month(self):
		admin_date = date(year=2016, month=4, day=12)
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

	def test_data_import(self):
		file_data = SimpleUploadedFile("data.csv", "file_content", content_type="text/csv")
		response = self.client.post(reverse('picu:data_import'), {'datafile': file_data})
		self.assertEqual(response.status_code, 200)
