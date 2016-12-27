from django.shortcuts import render, get_object_or_404

from .models import Admission, Patient


# Create your views here.

def index(request):
	# render - request, view, model
	return render(request, 'picu/index.html')


def admission_details(request, admission_id):
	admission_info = get_object_or_404(Admission, pk=admission_id)
	model = {"admission": admission_info}
	return render(request, 'picu/admission.html', model)


def patient_search(request):
	dob = request.POST['dob']
	if dob is None:
		patients = Patient.objects.all().filter(first_name__like=request.POST['first_name'], second_name__like=request.POST['second_name'])
	else:
		patients = Patient.objects.all().filter(first_name__like=request.POST['first_name'], second_name__like=request.POST['second_name'], date_of_birth=dob)

	model = {"patient_list": patients}
	return render(request, 'picu/index.html', model)


def new_admission(request):

	return render(request, 'picu/admission_form.html')
