from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from posthooks import handlers
import json

response_objects = {
	'SUCCESS':			{
		'CODE':		'200',
		'MESSAGE':	'Success, data recieved!'
	}
}

#
# payload(request)
# Here we handle incoming POST requests from /post/payload
#
@csrf_exempt
def payload(request):
	print request.META['HTTP_X_GITHUB_EVENT'];
	handlers.incoming(request.META['HTTP_X_GITHUB_EVENT'], json.loads(request.body))
	# handle request elsewhere to keep the view clean

	return HttpResponse(json.dumps(response_objects['SUCCESS']), mimetype = 'application/json')
	# we have our request and it matches up