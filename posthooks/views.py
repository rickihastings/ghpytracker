from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from posthooks import handlers
import json

response_objects = {
	'INVALID_REQUEST': 	{
		'CODE':		'500',
		'MESSAGE':	'You have sent an invalid request, this is odd!'
	},
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
	if 'payload' not in request.POST or request.POST['payload'] == '':
		return HttpResponse(json.dumps(response_objects['INVALID_REQUEST']), mimetype = 'application/json')
	# malformed request. ie doesn't have 'payload' or is invalid json

	handlers.incoming(request['X-Github-Event'], json.loads(request.POST['payload']))
	# handle request elsewhere to keep the view clean

	return HttpResponse(json.dumps(response_objects['SUCCESS']), mimetype = 'application/json')
	# we have our request and it matches up