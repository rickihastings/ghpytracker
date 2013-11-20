
message_reponses = {
	'commit':		"%s: <%s> %s: %s"
}

#
# push(post)
# Here we handle and parse JSON requests from github
#
def push(post):
	repo 	= post['repository']['name']
	# get the repository

	for commit in post['commits']:
		author		= commit['author']['email']
		commit_id	= commit['id'][:10]
		message		= commit['message']

		print message_reponses['commit'] % (repo, author, commit_id, message)
	# loop through the commits