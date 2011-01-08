"""This module allows channel operators to execute several commands through BBot, such as kicking, banning,
promoting and more. It can be used to manage channels on networks without services, such as EFnet."""

import q,api,config
class module(api.module):
	commands=['op','deop','kick','ban','unban','nick','echo','mode','voice','devoice','blacklist','unblacklist','listbl','whitelist','unwhitelist','topic']
	def __init__(self,server=config.network):
		self.blacklist=[]
		self.blconfig=open('trekbot/blacklist','r').readlines()
		for each in self.blconfig:
			self.blacklist.append(each.strip('\r\n'))
		self.whitelist=[]
		self.wlconfig=open('trekbot/whitelist','r').readlines()
		for each in self.wlconfig:
			self.whitelist.append(each.strip('\r\n'))
		del self.blconfig,self.wlconfig
		self.proxyscan=api.getConfigBool('trekbot','proxy-scan')
		api.module.__init__(self,server)
		
		self.su_funcs={
			'op':self.op,
			'deop':self.deop,
			'voice':self.voice,
			'devoice':self.devoice,
			'quiet':self.quiet,
			'unquiet':self.unquiet,
			'nick':self.nick,
			'mode':self.set_mode,
			'echo':self.echo,
			'say':self.echo,
			'topic':self.set_topic,
			'ban':self.set_ban,
			'unban':self.del_ban,
			'listbl':self.blacklist_list,
			'blacklist':self.blacklist_add,
			'unblacklist':self.blacklist_del,
			'listwl':self.whitelist_list,
			'whitelist':self.whitelist_add,
			'unwhitelist':self.whitelist_del,
			'kick':self.kick_user,
			'invite':self.invite_user,
		}
	def privmsg(self,nick,data,channel):
		ldata=data.lower()
		self.superuser=api.checkIfSuperUser(data,config.superusers)
		# Superuser Commands
		if self.superuser:
			if ' :%s'%config.cmd_char in data:
				command=data[data.find(' :%s'%config.cmd_char)+2+len(config.cmd_char):]
				param=None
				if ' ' in command:
					param=command[command.find(' ')+1:]
					command=command[:command.find(' ')]
				if command in self.su_funcs:
					self.su_funcs[command](nick,channel,param)
			elif ldata.find('?rehash')!=-1:
				self.__init__()
	def write_blacklist(self):
		self.blconfig=open('trekbot/blacklist','w')
		for each in self.blacklist:
			self.blconfig.write(each+'\n')
	def write_whitelist(self):
		self.wlconfig=open('trekbot/whitelist','w')
		for each in self.whitelist:
			self.wlconfig.write(each+'\n')
	def get_join(self,nick,channel,ip,user):
		if not ip in self.blacklist:
			if not ip in self.whitelist:
				if self.proxyscan:
					self.scan(ip,channel,nick)
				else:
					self.kick(nick,channel,'Sorry')
			else:
				self.mode(nick,channel,'+v')
		else:
			self.kick(nick,channel,'You are on the blacklist, please message a channel op about getting removed from the list')
	def scan(self,ip,channel,nick):
		self.scansafe=1
		try:
			print('Scanning '+ip)
			self.nm=nmap.PortScanner()
			#80, 8080, 1080, 3246
			self.nm.scan(ip,'808,23,1080,110,29505,8080,3246','-T5')
			for each in nm.all_hosts():
				print each+':::'
				lport = nm[each]['tcp'].keys()
				print lport
				if 808 in lport or 23 in lport or 110 in lport or 1080 in lport or 29505 in lport or 80 in lport or 8080 in lports or 3246 in lports:
					self.scansafe=0
					print 'DRONE'
			del self.nm
			if self.scansafe:
				self.mode(nick,channel,'+v')
		except:
			print 'PYTHON NMAP CRASH'
	
	# Superuser Commands
	def op(self,nick,channel,param=None):
		if not param:
			self.mode(nick,channel,'+o')
		else:
			self.mode(param,channel,'+o')
	def deop(self,nick,channel,param=None):
		if not param:
			self.mode(nick,channel,'-o')
		else:
			self.mode(param,channel,'-o')
	def voice(self,nick,channel,param=None):
		if not param:
			self.mode(nick,channel,'+v')
		else:
			self.mode(param,channel,'+v')
	def devoice(self,nick,channel,param=None):
		if not param:
			self.mode(nick,channel,'-v')
		else:
			self.mode(param,channel,'-v')
	def quiet(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: be careful or I will quiet you :P'%nick)
		else:
			self.mode(param,channel,'+q')
	def unquiet(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to tell me what to unquiet.  I can\'t unquiet [NULL]!'%nick)
		else:
			self.mode(param,channel,'-q')
	def nick(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to have a nick following the command'%nick)
		else:
			config.nick=param
			self.raw('NICK %s'%param)
	def set_mode(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to tell me what modes to set'%nick)
		else:
			self.mode('',channel,param)
	def echo(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: I can\'t echo nothing'%nick)
		else:
			self.msg(channel,param)
	def set_topic(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to specify a topic'%nick)
		else:
			self.raw('TOPIC %s :%s'%(channel,param))
	def set_ban(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to specify what to ban'%nick)
		else:
			self.mode(param,channel,'+b')
	def del_ban(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to specify what to unban'%nick)
		else:
			self.mode(param,channel,'-b')
	def kick_user(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to tell me who to kick'%nick)
		else:
			message=''
			if ' ' in param.strip(' '):
				message=param[param.find(' ')+1:]
				param=param[:param.find(' ')]
			else:
				message='You have been kicked from the channel.  (requested by %s)'%nick
			self.kick(param,channel,message)
	def invite_user(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to give me parameters for me to invite a user!'%nick)
		else:
			targetchan=''
			targetuser=''
			if ' ' in param:
				targetchan=param[param.find(' ')+1:]
				targetuser=param[:param.find(' ')]
			else:
				targetchan=channel
				targetuser=param
			self.raw('INVITE %s :%s'%(targetuser,targetchan))
	#Blacklist/Whitelist Commands - SuperUser Only
	def blacklist_list(self,nick,channel,param=None):
		self.msg(nick,str(self.blacklist))
	def blacklist_add(self,nick,channel,param=None):
		if not param in self.blacklist:
			self.blacklist.append(param)
			self.write_blacklist()
		else:
			self.msg(nick,'That host is already blacklisted.')
	def blacklist_del(self,nick,channel,param=None):
		if param in self.blacklist:
			self.blacklist.pop(self.blacklist.index(param))
			self.write_blacklist()
		else:
			self.msg(nick,'That host is not blacklisted.')
	def whitelist_list(self,nick,channel,param=None):
		self.msg(nick,str(self.whitelist))
	def whitelist_add(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to specify something to add to the whitelist.'%nick)
		else:
			if not param in self.whitelist:
				self.whitelist.append(param)
				self.write_whitelist()
			else:
				self.msg(nick,'That host is already whitelisted.')
	def whitelist_del(self,nick,channel,param=None):
		if not param:
			self.msg(channel,'%s: You need to specify something to remove from the whitelist.'%nick)
		else:
			if param in self.whitelist:
				self.whitelist.pop(self.whitelist.index(param))
				self.write_whitelist()
			else:
				self.msg(nick,'That host is not whitelisted.')