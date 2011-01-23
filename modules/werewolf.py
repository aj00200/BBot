"""This module is an IRC implementation of the Werewolf (a.k.a. Mafia) RPG party game
<http://en.wikipedia.org/wiki/Mafia_(party_game)>."""

import time
import api

class module(api.module):
	
	def __init__(self,address):
		api.module.__init__(self,address)
		
		self.game={
			'phase':'intro',
			'main_channel':api.getConfigStr('werewolf','main-channel'),
			'wolf_channel':api.getConfigStr('werewolf','wolf-channel'),
			'seer_channel':api.getConfigStr('werewolf','seer-channel')
			'players':{}			
		}
		self.waiting=[]
		self.commands={
			'join':self.join_game
		}
	def privmsg(self,nick,data,channel):
		if ' :%sw.'%config.cmd_char in data:
			command=data[data.find(' :%sw.'%config.cmd_char)+4+len(config.cmd_char):]
			if ' ' in command:
				params=command[command.find(' ')+1:]
				command=command[:command.find(' ')]
				
	# Public Commands
	def join_game(self,nick,channel,params=None):
		pass
	
	# Internal Methods
	def randomize_roles(self):
		pass
	
	def invite(self, player, channel):
		self.raw('INVITE %s %s'%(player,channel))
		
	def send_invites(self):
		count=0
		for player in self.game['players']:
			if self.game['players'][player] == 'villager':
				self.msg(player,'You are a villager. Every day phase, you can vote on who to lynch.')
			elif self.game['players'][player] == 'wolf':
				self.invite(player, self.game['wolf_channel'])
				self.msg(player,'You are a Werewolf. Every night phase, you and the other wolves decide on a victim to kill. Plese see the invite to %s'%self.game['wolf_channel'])
			elif self.game['players'][player] == 'seer':
				self.invite(player, self.game['seer_channel'])
				self.msg(player,'You are a seer. Every night phase, you and the other seers decide on a person to "see." You will then be told that person\'s role. Please see the invite to %s'%self.game['seer_channel'])