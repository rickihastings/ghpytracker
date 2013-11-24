import json
from django.conf import settings
from client_manager import startup

message_reponses = {
	'commit':			"%s by %s in %s: %s... (%s)",
	'commit_comment':	"%s has commented on %s in %s (%s)",
	'issue':			"%s has %s #%s in %s: %s... (%s)",
	'issue_comment':	"%s has commented on #%s: %s... in %s (%s)",
	'pull_request':		"%s has %s pull request #%s to merge %s into %s (%s)"
}

#
# incoming(post)
# Here we handle and parse JSON requests from github
#
def incoming(hook_type, post):
	try:
		post = json.loads(post)

		if hook_type == 'push':
			repo 		= post['repository']['owner']['name'] + '/' + post['repository']['name']
			# get the repository

			for commit in post['commits']:
				commit_id	= commit['id'][:7]
				author		= commit['author']['username']
				message		= ' '.join(commit['message'].split())[:100]
				url			= commit['url']

				resp(repo, message_reponses['commit'] % (commit_id, author, repo, message, url))
			# loop through the commits

		elif hook_type == 'commit_comment':
			user		= post['comment']['user']['login']
			commit_id	= post['comment']['commit_id'][:7]
			repo 		= post['repository']['full_name']
			url			= post['comment']['html_url']
			# get the repository

			resp(repo, message_reponses['commit_comment'] % (user, commit_id, repo, url))

		elif hook_type == 'issues':
			user		= post['issue']['user']['login']
			action		= post['action']
			number		= post['issue']['number']
			repo 		= post['repository']['full_name']
			title		= ' '.join(post['issue']['title'].split())[:100]
			url			= post['issue']['html_url']
			# get the repository

			resp(repo, message_reponses['issue'] % (user, action, number, repo, title, url))

		elif hook_type == 'issue_comment':
			user		= post['comment']['user']['login']
			number		= post['issue']['number']
			title		= ' '.join(post['issue']['title'].split())[:100]
			repo 		= post['repository']['full_name']
			url			= post['comment']['html_url']
			# get the repository

			resp(repo, message_reponses['issue_comment'] % (user, number, title, repo, url))

		elif hook_type == 'pull_request':
			repo 		= post['pull_request']['base']['repo']['full_name']
			user		= post['pull_request']['user']['login']
			action		= 'merged' if post['action'] == 'synchronize' else post['action'] 
			number		= post['pull_request']['number']
			head 		= post['pull_request']['head']['label']
			base 		= post['pull_request']['base']['label']
			url			= post['pull_request']['html_url']
			# get the repository

			resp(repo, message_reponses['pull_request'] % (user, action, number, base, head, url))
	except ValueError as e:
		return False

	return True

def resp(repo, text):
	channels = []

	for repository in settings.REPOS:
		if repo == repository['repo']:
			channels = repository['broadcast']
	# find the repository object first

	for channel in channels:
		split = channel.split(' ')
		network = split[0]
		channel = split[1]

		for key in startup.Startup.bots:
			bot = startup.Startup.bots[key]
			bot_network = bot['info']['server'] + ':' + str(bot['info']['port'])
			
			if bot_network == network:
				bot['client'].connection.privmsg(channel, text)
			# here we go, lets just send it away now, regardless of whether the channel exists
	# loop through the channels and grab a network relating to it