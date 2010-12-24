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
	def join_game(self,nick,channel,params=None)			
	# Internal Methods
	def randomize_roles(self):
		pass
	def send_invites(self):
		count=0
		for player in self.game['players']:
			if self.game['players'][player] == 'villiger':
				self.msg(player,'You are a villiger. Each day phase you can vote on who to kill')
			elif self.game['players'][player] == 'wolf':
				self.msg(player,'You are a Werewolf. Each night phase you and the other wolves decide on a victim to kill. Plese see the invite to %s'%self.game['wolf_channel'])
				self.raw('INVITE %s %s'%(player,self.game['wolf_channel']))
			elif self.game['players'][player] == 'seer':
				self.msg(player,'You are a seer. Each night phase, you and the other seers decide on a person to "see." You will be told if that person is a villager, a seer, or a wolf. Please see the invite to %s'%self.game['seer_channel'])
				self.raw('INVITE %s %s'%(player,self.game['seer_channel']))