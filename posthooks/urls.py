from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# incoming hook
	url(r'^payload$', 'posthooks.views.payload')
)