import os, threading, signal, httplib, json

from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from client_manager import ircbot

from github3 import login
from github3 import repos as ghrepos
# import required modules

"""
Startup()

Handles the client manager class, starting up, config validation and the startup of bots etc	
"""
class Startup(object):
	bots = {}
	gh = {}
	failed = False

	def __init__(self):
		if self.validate_config(settings.REPOS, settings.CLIENTS):
			self.proceed(settings.REPOS, settings.CLIENTS)
		# if validate passes then proceed

	def validate_config(self, repos, clients):
		if (type(clients) is not list or len(clients) == 0) or (type(repos) is not list or len(repos) == 0):
			print 'settings is not configured. Server will not boot, please configure it first!'
			os.kill(os.getpid(), signal.SIGTERM)
		# check if settings.CLIENTS exists and is a list

		def validate_setting(key, dicti, sid, name, eval_cond):
			if name not in dicti.keys() or dicti[name] == '' or (eval_cond != '' and eval(eval_cond)):
				print 'You have not properly configured %s in settings.%s[%s], see settings.py for instructions.' % (name, sid, key)
				os.kill(os.getpid(), signal.SIGTERM)
				self.failed = True
				return False
			else:
				return True

		key = 0
		for client in clients:
			if not validate_setting(key, client, 'CLIENTS', 'server', ''):
				break
			if not validate_setting(key, client, 'CLIENTS', 'port', 'type(dicti[name]) is not int'):
				break
			if not validate_setting(key, client, 'CLIENTS', 'nickname', ''):
				break
			if not validate_setting(key, client, 'CLIENTS', 'username', ''):
				break
			if not validate_setting(key, client, 'CLIENTS', 'realname', ''):
				break
			# basic validation, check each individual setting with validate_setting and handle accordingly.

			key = key + 1
		# loop through the clients and validate them

		key = 0
		for repo in repos:
			if not validate_setting(key, repo, 'REPOS', 'login', 'type(dicti[name]) is not tuple'):
				break
			if not validate_setting(key, repo, 'REPOS', 'repo', ''):
				break
			if not validate_setting(key, repo, 'REPOS', 'broadcast', 'type(dicti[name]) is not list'):
				break
			if not validate_setting(key, repo, 'REPOS', 'events', 'type(dicti[name]) is not list'):
				break

			key = key + 1
		# setup github pubsubdubhub hooks, or whatever the hell it's called.

		return not self.failed

	def proceed(self, repos, clients):
		key = 0
		for repo in repos:
			self.authenticate(repos[key]['login'][0], repos[key]['login'][1])
			# authenticate
			
			self.setup_hook(repos[key])
			key = key + 1
		# setup github hooks

		"""key = 0
		for client in clients:
			self.bots[key] = {}
			self.bots[key]['info'] = client
			#self.bots[key]['thread'] = threading.Thread(target=self.fork, args=(self.bots, key,))
			#self.bots[key]['thread'].start()
			self.fork(self.bots, key)

			key = key + 1
		# loop through the clients and set them up"""

	def authenticate(self, user, password):
		self.gh = login(user, password)

	def setup_hook(self, repo):
		url = repo['url']
		split = repo['repo'].split('/')
		owner = split[0]
		name = split[1]
		event_hooks = []

		Repository = self.gh.repository(owner, name)
		# get the repository info

		print Repository.create_hook('web', {
			'url': url,
			'content_type': 'json'
		}, repo['events'], True)

	def fork(self, bots, key):
		bots[key]['client'] = ircbot.IRCBot(bots[key]['info'])
		bots[key]['client'].start()
