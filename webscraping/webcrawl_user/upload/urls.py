from django.conf.urls import patterns, url
from upload import views

urlpatterns = patterns('',
	url(r'^$', views.home, name = 'home'),
	url(r'^logout/$', views.logout, name = 'logout'),
)
