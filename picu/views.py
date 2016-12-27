from django.shortcuts import render, get_object_or_404
from django.http import Http404

from datetime import datetime, timedelta

from .models import Admission


# Create your views here.

def index(request):
	#todays_admissions = Admission.objects.filter(picu_admission_date__gte=datetime.now()-timedelta(days=20))	
	admissions = Admission.objects.all()
	model = { "todays_admissions": admissions }
	# render - request, view, model
	return render(request, 'picu/index.html', model )
	
def admission(request, admission_id):
	admission = get_object_or_404(Admission, pk=admission_id)
	model = { "admission": admission }
	return render(request, 'picu/admission.html', model)
