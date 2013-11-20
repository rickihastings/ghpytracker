from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from posthooks import handlers
import json

valid_hosts 	 = ('207.97.227.253', '50.57.128.197', '108.171.174.178', '10.0.2.2')
response_objects = {
	'INVALID_HOST':		{
		'CODE': 	'500',
		'MESSAGE':	'You are not github!'
	},
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
# push(request)
# Here we handle incoming POST requests from /post/push
#
@csrf_exempt
def push(request):
	if request.META['REMOTE_ADDR'] not in valid_hosts:
		return HttpResponse(json.dumps(response_objects['INVALID_HOST']), mimetype = 'application/json')
	# got a request from someone other than github!

	if 'payload' not in request.POST or request.POST['payload'] == '':
		return HttpResponse(json.dumps(response_objects['INVALID_REQUEST']), mimetype = 'application/json')
	# malformed request. ie doesn't have 'payload' or is invalid json

	handlers.push(json.loads(request.POST['payload']))
	# handle request elsewhere to keep the view clean

	return HttpResponse(json.dumps(response_objects['SUCCESS']), mimetype = 'application/json')
	# we have our request and it matches up