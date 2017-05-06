import re

from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from picu import data_parser, summaries
from .forms import PatientSearchForm
from .models import Admission, Patient, Diagnosis


# Create your views here.
def index(request):
	# render - request, view, model
	form = PatientSearchForm(request.POST)
	model = {"patient_list": [], 'form': form}
	return render(request, 'picu/index.html', model)


def patient_search(request):

	if request.method == 'POST':
		my_form = PatientSearchForm(request.POST)

		if my_form.is_valid():
			dob = my_form.cleaned_data.get('date_of_birth') if not '' else None
			first_name = '%' if my_form.cleaned_data.get('first_name') is None else my_form.cleaned_data.get('first_name')
			second_name = '%' if my_form.cleaned_data.get('second_name') is None else my_form.cleaned_data.get('second_name')

			if dob is None:
				patients = Patient.objects.all().filter(first_name__icontains=first_name, second_name__icontains=second_name)
			else:
				patients = Patient.objects.all().filter(first_name__icontains=first_name, second_name__icontains=second_name, date_of_birth=dob)

			model = {'form': my_form, "patient_list": patients}
			return render(request, 'picu/index.html', model)
		else:
			raise Exception("*********** form is not valid todo return page with the errors ************* ")
	else:
		return render(request, 'picu/index.html', {"patient_list": [], 'form': PatientSearchForm})


def patient_view(request, id):

	patient = get_object_or_404(Patient, id=id)
	# - indicates descending order we want admissions listed most recent first
	admission_list = Admission.objects.filter(patient_id=id).order_by('-picu_admission_date')
	model = {'patient': patient, 'admission_list': admission_list }
	return render(request, 'picu/patient_details.html', model)

def admission_add(request):
	request.session['URL_HISTORY'] = []
	return redirect(reverse('admin:picu_admission_add'))

def diagnosis_search(request):
	search_param = request.GET.get('criteria', '')
	if search_param:
		diagnosis_list = Diagnosis.objects.filter(name__contains=search_param)
		data = serializers.serialize("json", diagnosis_list)
		return HttpResponse(data)
	return None

def summary_reports(request, year=None):

	if not year:
		year = timezone.now().year
	results = summaries.total_year_admissions(year)
	monthly_admission_list = results['admissions']
	totals_summary = results['totals']
	boys = results['boys']
	girls = results['girls']
	deaths = results['deaths']
	discharges = results['discharges']
	ventilations = results['ventialtions']
	years = []
	for x in range(timezone.now().year-10, timezone.now().year+1):
		years.extend([x])

	return render(request, 'picu/summary_reports.html', {'admissions': monthly_admission_list.items(), 'totals': totals_summary.items(),
	                                                     'year': int(year), 'boys': boys.items(), 'girls': girls.items(), 'deaths': deaths.items(),
	                                                     'discharges': discharges.items(), 'ventilations': ventilations.items(),
	                                                     'total_days': results['total_days'].items(), 'hospital': 'needs to go into the session',
	                                                     'years': years, 'sum_admissions': results['sum_admissions'], 'sum_discharges': results['sum_discharges'],
	                                                     'sum_girls': results['sum_girls'], 'sum_boys': results['sum_boys'],
	                                                     'sum_ventilated': results['sum_ventilated'], 'sum_deaths': results['sum_deaths'],
	                                                     'sum_patient_days': results['sum_patient_days']})

def data_import(request):

	if request.method == 'POST' and request.FILES['datafile']:
		csvfile = request.FILES['datafile']
		contents = csvfile.read().decode('utf-8')
		rows = re.split('\n', contents)

		for i, row in enumerate(rows):
			if i is 0:
				continue

			cells = row.split(',') # expect 33 columns
			if len(cells) == 33:
				data_parser.create_admission(cells)

		fs = FileSystemStorage()
		filename = fs.save(csvfile.name, csvfile)
		uploaded_file_url = fs.url(filename)

		return HttpResponse("Success! " + str(uploaded_file_url))

	return HttpResponse(status=500)
