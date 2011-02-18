import config
backend=getattr(__import__('backends.%s'%config.backend),config.backend)
def get_config_str(cat,name):
	return config.c.get(cat,name)
def get_config_int(cat,name):
	return config.c.getint(cat,name)
def get_config_float(cat,name):
	return config.c.getfloat(cat,name)
def get_config_bool(cat,name):
	return config.c.getboolean(cat,name)
def get_host(data):
	'''Returns the hostname (IP address) of the person who sent the message passed to the variable data'''
	return data[data.find('@')+1:data.find(' ')]
def get_nick(data):
	'''Returns the nickname of the person who sent the message passed to this function'''
	return data[1:data.find('!')]
def get_ident(data):
	'''Returns the ident of the person who sent the message passed to this function'''
	return data[data.find('!')+1:data.find('@')]
def get_message(data):
	'''Returns the actual message that was sent without the nickname, hostname, and so on'''
	return data[data.find(' :')+2:]
def host_in_list(data,list):
	'''Tells you if the host of the person who sent the message that is pased as the first arg is in the list of hosts which is the second arg'''
	host=get_host(data)
	for su in list:
		if host.find(su)!=-1:
			return True
	else:
		return False
def check_if_super_user(data,superusers=config.superusers):
	return host_in_list(data,superusers)
def load_module(server,module):
	return backend.connections[server].load_module(module)

# Command List
commands={}
def register_commands(address,cmds):
	if address not in commands:
		commands[address]=[]
	try:
		for cmd in cmds:
			if cmd not in commands[address]:
				commands[address]+=[cmd]
	except:
		pass
def get_command_list(address):
	try:
		return commands[address]
	except:
		return 'There was an error processing your request'

# Hooks
hooks={}
def hook_command(name,callback,server):
	'''Hook a command for use by the backend, using this when possible will increase the speed of the bot and your module'''
	if (server not in hooks):
		return False
	elif (name in hooks[server]):
		return False
	try:
		hooks[name]=callback
		return True
	except:
		return False
# Base Module
class module(object):
	'''Base class that all modules should use to maintain best compatibility with future versions of the API'''
	def __init__(self,address):
		self.__address__=address
	# Receive
	def privmsg(self,nick,data,channel):
		'''Called every time a PRIVMSG is recieved.
			nick: the nickname of the person sending the message
			data: the raw data recieced (without the line ending)
			channel: the channel the message was recieved in'''
		pass
	def get_notice(self,nick,data,channel):
		'''Called every time a notice is recieved'''
		pass
	def get_join(self,nick,user,host,channel):
		pass
	def get_raw(self,type,params):
		'''Called every time a message that does not fall into the other categories is recieved:
			type is set to 'CODE' when messages that corespond to a numberic code are recieved
			type is set to 'MODE' when a mode is changed'''
		pass
	# Send
	def msg(self,channel,data=' '):
		'''Send a message, data, to channel
			Example: self.msg('#bbot','Hello world!')'''
		self.raw('PRIVMSG %s :%s\r\n'%(channel,data))
	def notice(self,channel,data):
		'''Send a notice to a channel
			Example: self.notice('#bbot','A new BBot version has been released')'''
		self.raw('NOTICE %s :%s\r\n'%(channel,data))
	def join(self,channel):
		'''Have BBot join a channel:
			Example: self.join('#bbot')'''
		self.raw('JOIN %s\r\n'%channel)
	def part(self,channel,message='BBot the IRC Bot'):
		'''Have BBot part a channel
			Example: self.part('#bbot')'''
		self.raw('PART %s :%s\r\n'%(channel,message))
	def kick(self,nick,channel,message=''):
		'''Kick a person out of a channel
			Example: self.kick('spammer','#bbot','Spam is not allowed in #bbot')'''
		self.raw('KICK '+channel+' '+nick+' :'+message+'\r\n')
	def mode(self,nick,channel,mode):
		'''Set the mode, mode, on nick in channel. If you want to set a normal channel mode, set nick to ''.'''
		self.raw('MODE '+channel+' '+mode+' '+nick+'\r\n')
	def raw(self,data):
		'''Send raw data to the server
			Example: self.raw('PRIVMSG #bbot :This is a raw message')
			Note: the line ending is not required'''
		backend.connections[self.__address__].push('%s\r\n'%(data))
		print 'Send: %s'%data
