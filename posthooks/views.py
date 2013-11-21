import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from posthooks import handlers

response_objects = {
	'SUCCESS':			{
		'CODE':		'200',
		'MESSAGE':	'Success, data recieved!'
	},
	'ERROR':			{
		'CODE':		'500',
		'MESSAGE':	'Error has occured, BYE NOW'
	}
}

#
# payload(request)
# Here we handle incoming POST requests from /post/payload
#
@csrf_exempt
def payload(request):
	response = handlers.incoming(request.META['HTTP_X_GITHUB_EVENT'], request.body)
	# handle request elsewhere to keep the view clean

	if response == False:
		code = json.dumps(response_objects['ERROR'])
	else:
		code = json.dumps(response_objects['SUCCESS'])

	return HttpResponse(code, content_type = 'application/json')
	# we have our request and it matches up