from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# push hook
	url(r'^push$', 'posthooks.views.push')
)