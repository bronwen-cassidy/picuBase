from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Admission


# Create your views here.

def index(request):
	#todo this will not remain as such we will be displaying a graph (possibly daily admisison count?)
	todays_admissions = Admission.objects.filter(picu_admission_date__gte=datetime.now()-timedelta(days=20))
	template = loader.get_template('picu/index.html')
	context = RequestContext(request, { 'todays_admissions': todays_admissions, } )
	return HttpResponse(template.render(context))
