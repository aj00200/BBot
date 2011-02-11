"""This module allows for easy factoid tracking a la Infobot, in addition to
generating URLs for common websites, such as Google SSL, Wikipedia SSL and
aj00200's Knowledge Base. It also allows the admin to execute functions like
loading modules, connecting to other networks and more. Additionally, it can
output important BBot information like its version."""

import api,re,config
import bbot as BBot
import time,thread,json
try:
	f=open('database.json')
	dict=json.load(f)
	f.close()
	del f
except:
	dict={}
class module(api.module):
	goog_str='https://encrypted.google.com/search?q=%s'
	wiki_str='https://secure.wikimedia.org/wikipedia/en/wiki/%s'
	stop_words=[
		' a ',' the ',' was ',' an '
	]
	is_words=[
		' was ',' are ',' am '
	]
	def __init__(self,server):
		api.module.__init__(self,server)
		api.register_commands(self.__address__,['goog','wiki','hit','add','del','writedb','load','reload','version','connect','py'])
		self.command_list=[]
		self.command_start=':'+config.cmd_char
		self.funcs={
			'hit':self.hit,
			'version':self.version,
			'goog':self.goog,
			'wiki':self.wiki,
			'help':self.help
		}
		self.sufuncs={
			'join':self.su_join,
			'writedb':self.su_writedb,
			'raw':self.su_raw,
			'part':self.su_part,
			'add':self.su_add,
			'load':self.su_load,
			'reload':self.su_reload,
			'py':self.su_py,
			'connect':self.su_connect,
			'del':self.su_del
		}
		self.lnick=config.nick.lower()
	def __destroy__(self):
		pass
	def privmsg(self,nick,data,channel):
		if '#' not in channel: #if message is a pm
			channel=nick
		ldata=data.lower()

		#Check if message is a command
		if self.command_start in data:
			cmd=data[data.find(self.command_start)+len(self.command_start):]
			if ' ' in cmd:
				cmd=cmd[:cmd.find(' ')]

			#Superuser Commands
			if api.checkIfSuperUser(data):
				if ' > ' in data:
					channel=data[data.find(' > ')+3:]
					data=data[:data.find(' > ')]
				if cmd in self.sufuncs:
					self.sufuncs[cmd](nick,data,channel)
	
			#Normal Commands
			if cmd in self.funcs:
				if ' | ' in data:
					nick=data[data.find(' | ')+3:]
				self.funcs[cmd](nick,data,channel)
			else:
				cmd=data[data.find(self.command_start)+len(self.command_start):]
				if ' | ' in cmd:
					nick=cmd[cmd.find(' | ')+3:]
					cmd=cmd[:cmd.find(' | ')]
				self.query(cmd,nick,channel)

		#Check if I've been pinged
		if (' :%s: '%self.lnick in ldata) or (' :%s, '%self.lnick in ldata):
			q=ldata[ldata.find(self.lnick)+len(self.lnick)+2:]
			self.query(q,nick,channel)
			return 0

		#Answer basic questions
		ldata=ldata.replace('whats','what is')
		if re.search('(what|where|who) (is|was|are|am)',ldata):
			for word in self.stop_words:
				ldata=ldata.replace(word,' ')
			for word in self.is_words:
				ldata=ldata.replace(word,' is ')
			q=ldata[ldata.find(' is ')+4:].strip('?')
			self.query(q,nick,channel)

		#Version ping
		elif '\x01VERSION\x01' in data:
			self.notice(nick,'\x01VERSION BBot Version %s\x01'%BBot.version)

		#Prefix ping - responds with the current command char
		elif '\x01PREFIX\x01' in data:
			self.notice(nick,'\x01PREFIX My current command character is: %s\x01'%config.cmd_char)
	def get_raw(self,t,d):
		if t == 'CODE':
			if d[0] == '433':
				# Nick is already in use
				self.raw('NICK %s_'%config.nick)
				if api.getConfigBool('main','use-services'):
					self.msg('NickServ','GHOST %s %s'%(config.nick,config.password))
					time.sleep(api.getConfigFloat('main','wait-after-identify'))
					self.raw('NICK %s'%config.nick)
	def add_factoid(self,query,nick):
		tmp=query
		try:
			if '<ACTION>'in query[1]:
				tmp[1]=str(tmp[1].replace('<ACTION>','\x01ACTION ')+'\x01')
			dict[query[0]]=query[1]
			return True
		except IndexError:
			return False
	def del_factoid(self,query):
		if query in dict:
			del dict[query]
	def write_dict(self):
		f=open('database.json','w')
		f.write(json.dumps(dict))
		f.close()
	def read_dict(self):
		f=open('database.json')
		dict=json.load(f)
		f.close()
	def query_dict(self,query):
		'''Primarily for the unittester	'''
		if query.lower() in dict:
			return str(dict[query.lower()])
	def query(self,query,nick,channel):
		'''Querys the database for the factoid 'query', and returns its value to the channel if it is found'''
		q=unicode(query.lower())
		if q in dict:
			self.msg(channel,str(dict[q].replace('%n',nick)))

	#////////Single Functions/////////
	def hit(self,nick,data,channel):
		'''Causes BBot to punch someone'''
		if 'hit ' in data:
			who=data[data.find('hit ')+4:]
			self.msg(channel,'\x01ACTION punches %s\x01'%who)
	def version(self,nick,data,channel):
		'''Sends the version number to the channel'''
		self.msg(channel,'I am version %s'%BBot.version)
	def goog(self,nick,data,channel):
		if 'goog ' in api.getMessage(data):
			w=str(data[data.find('goog ')+5:].replace(' ','+'))
			self.msg(channel,self.goog_str%w)
	def wiki(self,nick,data,channel):
		if 'wiki ' in api.getMessage(data):
			w=data[data.find('wiki ')+5:].replace(' ','_')
			self.msg(channel,self.wiki_str%w)
	def help(self,nick,data,channel):
		self.msg(channel,'%s: %s'%(nick,', '.join(api.get_command_list(self.__address__))))
	def su_join(self,nick,data,channel):
		'''Makes BBot join the channel which is the param'''
		self.raw('JOIN %s'%data[data.find('join ')+5:])
	def su_writedb(self,nick,data,channel):
		'''Writes the factoids database to the harddrive'''
		self.write_dict()
		self.notice(channel,'<<Wrote Database>>')
	def su_raw(self,nick,data,channel):
		self.raw(data[data.find('raw ')+4:])
	def su_part(self,nick,data,channel):
		self.raw('PART %s'%data[data.find('part ')+5:])
	def su_add(self,nick,data,channel):
		query=data[data.find(' :')+2:]
		query=query[query.find('add ')+4:].split(':::')
		if self.add_factoid(query,nick):
			self.notice(channel,'<<Added %s>>'%query)
		else:
			self.msg(channel,'%s: Adding of the factoid failed. Make sure you are using the proper syntax.'%nick)
	def su_load(self,nick,data,channel):
		query=data[data.find(' :')+2:]
		query=query[query.find('load ')+5:]
		if api.load_module(self.__address__,query):
			self.notice(channel,'<<Loaded %s>>'%query)
		else:
			self.notice(channel,'Error loading %s'%query)
	def su_py(self,nick,data,channel):
		if 'py ' not in data:
			self.msg(channel,'%s: ...'%nick)
			return
		self.q=data[data.find('py ')+3:]
		try:
			ret=str(eval(self.q))
		except Exception,e:
			ret='<<Error %s; %s>>'%(type(e),e.args)
		self.msg(channel,ret)
	def su_connect(self,nick,data,channel):
		tmp=data[data.find('connect ')+8:]
		self.notice(channel,'<<Connecting to %s>>'%tmp)
		api.backend.connect(tmp,6667,False)
	def su_reload(self,nick,data,channel):
		tmp=data[data.find('reload ')+7:]
		thread.start_new_thread(api.backend.connections[self.__address__].reload_module,(tmp,))
		self.notice(channel,'<<Reloaded %s>>'%tmp)
	def su_del(self,nick,data,channel):
		tmp=data[data.find('del ')+4:]
		self.del_factoid(tmp)
		self.notice(channel,'<<Delete %s>>'%tmp)
