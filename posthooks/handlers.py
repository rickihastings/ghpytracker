from client_manager import startup

message_reponses = {
	'commit':			"%s by %s in %s: %s (%s)",
	'commit_comment':	"%s has commented on %s in %s (%s)",
	'issue':			"%s has %s #%s in %s: %s (%s)",
	'issue_comment':	"%s has commented on #%s: %s in %s (%s)",
	'pull_request':		"%s has %s pull request #%s to merge %s into %s (%s)"
}

#
# incoming(post)
# Here we handle and parse JSON requests from github
#
def incoming(hook_type, post):
	if hook_type == 'push':
		repo 		= post['repository']['owner']['name'] + '/' + post['repository']['name']
		# get the repository

		for commit in post['commits']:
			commit_id	= commit['id'][:7]
			author		= commit['author']['username']
			message		= commit['message']
			url			= commit['url']

			resp(message_reponses['commit'] % (commit_id, author, repo, message, url))
		# loop through the commits

	elif hook_type == 'commit_comment':
		user		= post['comment']['user']['login']
		commit_id	= post['comment']['commit_id'][:7]
		repo 		= post['repository']['full_name']
		url			= post['comment']['html_url']
		# get the repository

		resp(message_reponses['commit_comment'] % (user, commit_id, repo, url))

	elif hook_type == 'issues':
		user		= post['issue']['user']['login']
		action		= post['action']
		number		= post['issue']['number']
		repo 		= post['repository']['full_name']
		title		= post['issue']['title']
		url			= post['issue']['html_url']
		# get the repository

		resp(message_reponses['issue'] % (user, action, number, repo, title, url))

	elif hook_type == 'issue_comment':
		user		= post['comment']['user']['login']
		number		= post['issue']['number']
		title		= post['issue']['title']
		repo 		= post['repository']['full_name']
		url			= post['comment']['html_url']
		# get the repository

		resp(message_reponses['issue_comment'] % (user, number, title, repo, url))

	elif hook_type == 'pull_request':
		user		= post['pull_request']['user']['login']
		action		= 'merged' if post['action'] == 'synchronize' else post['action'] 
		number		= post['pull_request']['number']
		head 		= post['pull_request']['head']['label']
		base 		= post['pull_request']['base']['label']
		url			= post['pull_request']['html_url']
		# get the repository

		resp(message_reponses['pull_request'] % (user, action, number, base, head, url))

def resp(text):
	print text
	#print startup.Startup.bots
	# we have a response, send it to a channel based on the repo