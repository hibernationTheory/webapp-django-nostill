from django.conf.urls import url, patterns
from nostill import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^submit/$', views.submit, name = 'submit'),
	url(r'^login/$', views.login, name='login'),
	)