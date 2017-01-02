from django.shortcuts import render, get_object_or_404

from .models import Admission, Patient
from .forms import PatientSearchForm

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
			dob = my_form.cleaned_data.get('dob') if not '' else None
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

