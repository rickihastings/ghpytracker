
message_reponses = {
	'commit':			"%s: <%s> %s: %s (%s)",
	'commit_comment':	"%s has commented on %s in %s (%s)",
	'issue':			"%s has %s #%s in %s: %s (%s)",
	'issue_comment':	"%s has commented on #%s (%s) in %s (%s)",
	'pull_request':		"%s has %s #%s in %s: %s (%s)"
}

#
# incoming(post)
# Here we handle and parse JSON requests from github
#
def incoming(hook_type, post):
	if hook_type == 'push':
		repo 		= post['repository']['full_name']
		# get the repository

		for commit in post['commits']:
			author		= commit['author']['email']
			commit_id	= commit['id'][:7]
			message		= commit['message']
			url			= commit['url']

			print message_reponses['commit'] % (repo, author, commit_id, message, url)
		# loop through the commits

	else if hook_type == 'commit_comment':
		user		= post['comment']['user']['login']
		commit_id	= post['comment']['id'][:7]
		repo 		= post['repository']['full_name']
		url			= post['comment']['html_url']
		# get the repository

		print message_reponses['commit_comment'] % (user, commit_id, repo, url)

	else if hook_type == 'issues':
		user		= post['issue']['user']['login']
		action		= post['action']
		number		= post['issue']['number']
		repo 		= post['repository']['full_name']
		title		= post['issue']['title']
		url			= post['issue']['html_url']
		# get the repository

		print message_reponses['issue'] % (user, action, number, repo, title, url)

	else if hook_type == 'issue_comment':
		user		= post['comment']['user']['login']
		number		= post['issue']['number']
		title		= post['issue']['title']
		repo 		= post['repository']['full_name']
		url			= post['comment']['html_url']
		# get the repository

		print message_reponses['issue_comment'] % (user, number, title, repo, url)

	else if hook_type == 'pull_request':
		user		= post['comment']['user']['login']
		number		= post['pull']['number']
		title		= post['pull']['title']
		repo 		= post['repository']['full_name']
		url			= post['comment']['html_url']
		# get the repository

		print message_reponses['pull_request'] % (user, number, title, repo, url)
