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

	def on_privmsg(self, c, e):
		self.do_command(e, e.arguments()[0])

	def do_command(self, e, cmd):
		print cmd
		nick = e.source.nick
		c = self.connection

		if cmd == "disconnect":
			self.disconnect()
		elif cmd == "die":
			self.die()
		else:
			c.notice(nick, "Not understood: " + cmd)