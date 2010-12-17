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
			'nick':self.nick,
			'mode':self.set_mode,
			'echo':self.echo,
			'say':self.echo,
			'topic':self.set_topic,
			'ban':self.set_ban,
			'unban':self.del_ban,
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
			#Blacklist
			elif ':?blacklist ' in data:
				name=data[data.find('?blacklist ')+11:]
				if not name in self.blacklist:
					self.blacklist.append(name)
					self.write_blacklist()
			elif ':?unblacklist ' in ldata:
				name=data[data.find('?unblacklist ')+13:]
				if name in self.blacklist:
					self.blacklist.pop(self.blacklist.index(name))
					self.write_blacklist()
				else:
					self.msg(nick,'That host is not blacklisted')
			elif ':?listbl' in ldata:
				self.msg(nick,str(self.blacklist))
			elif ':?whitelist ' in ldata:
				name=data[data.find('?whitelist ')+11:]
				if not name in self.whitelist:
					self.whitelist.append(name)
					self.write_blacklist()
			elif ':?unwhitelistlist ' in ldata:
				name=data[data.find('?unwhitelist ')+13:]
				if name in self.blacklist:
					self.whitelist.pop(self.blacklist.index(name))
					self.write_whitelist()
				else:
					self.msg(nick,'That host is not whitelisted')
			elif ':?listbl' in ldata:
				self.msg(nick,str(self.blacklist))
	def write_blacklist(self):
		self.blconfig=open('trekbot/blacklist','w')
		for each in self.blacklist:
			self.blconfig.write(each+'\n')
	def write_whitelist(self):
		self.wlconfig=open('trekbot/whitelist','w')
		for each in self.whitelist:
			self.wlconfig.write(each+'\n')
	def get_join(self,nick,channel,ip,user):
		print "GOT JOIN"
		
		if not ip in self.blacklist:
			if not ip in self.whitelist:
				if self.proxyscan:
					self.scan(ip,channel,nick)
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