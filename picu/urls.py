"""
	picu base urls
"""
from django.conf.urls import url
from django.contrib import auth
from django.contrib.auth import views
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index' ),
	url(r'^admission/(\d+)/', views.admission_details, name='admission' ),
    url(r'^admission/add/', views.new_admission, name='new_admission' ),
	url(r'^patient_search/', views.patient_search, name='patient_search' ),
	url(r'^admin/login/', auth.views.login, kwargs={"template_name":"admin/login.html"}, name='login'),
]