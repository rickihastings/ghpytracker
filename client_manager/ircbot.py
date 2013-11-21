import sys, os
import irc.bot

"""
IRCBot()

An class for each individual irc bots, handles the creation of them, assigns any listener functions
and provides an interface to use them.
"""
class IRCBot(irc.bot.SingleServerIRCBot):
	def __init__(self, client):
		irc.bot.SingleServerIRCBot.__init__(self, [(client['server'], client['port'])], client['nickname'], client['username'], client['realname'])
		self.server 	= client['server']
		self.port 		= client['port']
		self.nickname 	= client['nickname']
		self.username 	= client['username']
		self.realname 	= client['realname']
		self.chans 		= client['channels']

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + '_')

	def on_welcome(self, c, e):
		for channel in self.chans:
			c.join(channel['channel'], channel['key'])

	def on_pubmsg(self, c, e):
		print c, e