"""This provides a two-way bridge between two channels on different networks."""

import q
import api
class module(api.module):
	commands=[]
	chan='#bbot'
	net1='irc.fossnet.info'
	net2='irc.freenode.net'
	def __init__(self,server):
		self.
		api.module.__init__(self,server)
	def privmsg(self,nick,data,channel):
		if channel==self.chan:
			if self.__server__==self.net1:
				self.to=self.net2
			elif self.__server__==self.net2:
				self.to=self.net1
			else:
				self.to=self.net1
			try:
				q.append(self.to,(channel,'<%s> %s'%(nick,data[data.find(' :')+2:])))
			except Exception:
				pass
