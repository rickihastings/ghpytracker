import sys, os, re
import irc.bot
import github3

from django.conf import settings

"""
IRCBot()

An class for each individual irc bots, handles the creation of them, assigns any listener functions
and provides an interface to use them.
"""
class IRCBot(irc.bot.SingleServerIRCBot):
	def __init__(self, client, startup):
		irc.bot.SingleServerIRCBot.__init__(self, [(client['server'], client['port'])], client['nickname'], client['username'], client['realname'])
		self.server 	= client['server']
		self.port 		= client['port']
		self.nickname 	= client['nickname']
		self.username 	= client['username']
		self.realname 	= client['realname']
		self.chans 		= client['channels']
		self.startup 	= startup

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + '_')

	def on_welcome(self, c, e):
		for channel in self.chans:
			c.join(channel['channel'], channel['key'])

	def on_pubmsg(self, c, e):
		chan = e._target
		msg = e._arguments[0]
		regex = re.compile(r".*(\b[0-9a-f]{40}\b|\b[0-9a-f]{7}\b).*", re.IGNORECASE)
		regex2 = re.compile(r".*\bcommit\b.*", re.IGNORECASE)

		search = regex.search(msg)
		if search and regex2.search(msg):
			commit_sha = search.group(1)
			
			for repo in settings.REPOS:
				repository = self.startup.Repositories[repo['repo']]
				commit = repository.commit(commit_sha)
				# get commit

				if type(commit) is github3.repos.commit.RepoCommit:
					url = commit.html_url
					commit = commit.commit
					message = ' '.join(commit.message.split())[:50]

					c.privmsg(chan, "Commit %s: %s... (%s)" % (commit_sha, message, url))
		# we've found a commit number match

		regex = re.compile(r"([#?])([0-9]+)\b")
		regex2 = re.compile(r".*\b(issue|pull)\b.*", re.IGNORECASE)
		
		search = regex.search(msg)
		if search and regex2.search(msg):
			issue_id = int(search.group(2))

			for repo in settings.REPOS:
				repository = self.startup.Repositories[repo['repo']]
				issue = repository.issue(issue_id)
				# get issue

				if type(issue) is github3.issues.issue.Issue:
					title = ' '.join(issue.title.split())[:50]
					c.privmsg(chan, "Issue #%s: %s... (%s)" % (search.group(2), title, issue.html_url))
		# we found an issue number match