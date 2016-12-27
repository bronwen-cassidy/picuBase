"""
	picu base urls
"""
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index' ),
	url(r'^admission/(\d+)/', views.admission, name='admission' ),
]