"""
	picu base urls
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.index, name='index' ),
	url(r'^patient/search/', views.patient_search, name='patient_search' ),
]