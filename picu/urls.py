"""
picu base urls
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': 'login/'}, name='logout'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.index, name='index'),
	url(r'^patient/search/', views.patient_search, name='patient_search'),
	url(r'^patient/(?P<id>\w+)/view/$', views.patient_view, name='patient_view'),
]