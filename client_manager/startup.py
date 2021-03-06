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
	Repositories = {}

	def __init__(self):
		if self.validate_config(settings.REPOS, settings.CLIENTS):
			self.proceed(settings.REPOS, settings.CLIENTS)
		# if validate passes then proceed

	def validate_config(self, repos, clients):
		if os.environ.get('GITHUB_TOKEN') == None:
			print 'the enrivoment variable GITHUB_TOKEN is not set'
			os.kill(os.getpid(), signal.SIGTERM)
		# we need a github username and password, this needs to be in the enviroment vars, not settings

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

		for key in clients:
			if not validate_setting(key, key, 'CLIENTS', 'server', ''):
				break
			if not validate_setting(key, key, 'CLIENTS', 'port', 'type(dicti[name]) is not int'):
				break
			if not validate_setting(key, key, 'CLIENTS', 'nickname', ''):
				break
			if not validate_setting(key, key, 'CLIENTS', 'username', ''):
				break
			if not validate_setting(key, key, 'CLIENTS', 'realname', ''):
				break
			# basic validation, check each individual setting with validate_setting and handle accordingly.
		# loop through the clients and validate them

		for key in repos:
			if not validate_setting(key, key, 'REPOS', 'repo', ''):
				break
			if not validate_setting(key, key, 'REPOS', 'broadcast', 'type(dicti[name]) is not list'):
				break
			if not validate_setting(key, key, 'REPOS', 'events', 'type(dicti[name]) is not list'):
				break
		# setup github pubsubdubhub hooks, or whatever the hell it's called.

		return not self.failed

	def proceed(self, repos, clients):
		self.authenticate(os.environ['GITHUB_TOKEN'])
		# authenticate

		for repo in repos:
			self.setup_hook(repo)
		# setup github hooks

		key = 0
		for client in clients:
			self.bots[key] = {}
			self.bots[key]['info'] = client
			self.bots[key]['thread'] = threading.Thread(target=self.fork, args=(self.bots, key))
			self.bots[key]['thread'].start()
			key = key + 1
		# loop through the clients and set them up

	def authenticate(self, password):
		self.gh = login(token=password)

	def setup_hook(self, repo):
		url = repo['url']
		split = repo['repo'].split('/')
		owner = split[0]
		name = split[1]
		event_hooks = []

		Repository = self.gh.repository(owner, name)
		self.Repositories[repo['repo']] = Repository
		# get the repository info

		for hook in Repository.iter_hooks():
			if hook.name == 'web':
				hook.delete()
		# remove hooks otherwise we get validation error if we try to readd them

		Repository.create_hook('web', {
			'url': url,
			'content_type': 'json'
		}, repo['events'], True)

	def fork(self, bots, key):
		bots[key]['client'] = ircbot.IRCBot(bots[key]['info'], self)
		bots[key]['client'].start()
