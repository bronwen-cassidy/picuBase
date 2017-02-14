import re

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from picu import dataParser
from .forms import PatientSearchForm
from .models import Admission, Patient


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


def data_import(request):

	if request.method == 'POST' and request.FILES['datafile']:
		csvfile = request.FILES['datafile']
		contents = csvfile.read().decode('utf-8')
		rows = re.split('\n', contents)

		for i, row in enumerate(rows):
			if i is 0:
				continue

			cells = row.split(',')
			if len(cells) > 0:
				dataParser.create_admission(cells)

		fs = FileSystemStorage()
		filename = fs.save(csvfile.name, csvfile)
		uploaded_file_url = fs.url(filename)

		return HttpResponse("Success! " + str(uploaded_file_url))

	return HttpResponse(status=500)
