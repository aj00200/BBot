import q,api,re,config
import bbot as BBot
import time,thread,sqlite3
dict=sqlite3.connect('bbot.sqlite3')
class module(api.module):
	commands=['help','goog','wiki','pb','upb','kb','hit','?<query>','add','del','writedict','load','reload','version','connect','py']
	goog_str='https://encrypted.google.com/search?q=%s'
	wiki_str='https://secure.wikimedia.org/wikipedia/en/wiki/%s'
	kb_str='http://www.kb.aj00200.heliohost.org/index.py?q=%s'
	stop_words=[
		' a ',' the ',' was ',' an '
	]
	is_words=[
		' was ',' are ',' am '
	]
	def get_command_list(self):
		try:
			time.sleep(5)
			for module in BBot.networks[config.network]:
				for command in module.commands:
					self.command_list.append(command)
		except Exception,e:
			print 'Error: %s; with args: %s;'%(type(e),e.args)
	def __init__(self,server):
		self.command_list=[]
		self.command_start=':'+config.cmd_char
		#thread.start_new_thread(self.get_command_list,())
		self.read_dict()
		self.funcs={
			'hit':self.hit,
			'version':self.version,
			'goog':self.goog,
			'wiki':self.wiki,
			'kb':self.kb
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
		api.module.__init__(self,server)
	def __destroy__(self):
		dict.close()
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
				if cmd in self.sufuncs:
					self.sufuncs[cmd](nick,data,channel)
	
			#Normal Commands
			if cmd in self.funcs:
				if ' | ' in data:
					nick=data[data.find(' | ')+3:]
				self.funcs[cmd](nick,data,channel)
			else:
				self.query(cmd,nick,channel)
		#Check if I've been pinged
		if re.search(':'+re.escape(self.lnick)+'[:,]',ldata):
			q=ldata[ldata.find(self.lnick)+len(self.lnick):]
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
		#Help command
		elif self.command_start+'help' in data:
			self.msg(channel,'%n: Sorry, but help is not available at this time')
		#Version ping
		elif '\x01VERSION\x01' in data:
			self.notice(nick,'\x01VERSION BBot Version %s\x01'%BBot.version)
	def add_factoid(self,query,nick):
		tmp=query
		if '<ACTION>'in query[1]:
			tmp[1]=str(tmp[1].replace('<ACTION>','\x01ACTION ')+'\x01')
		self.c.execute('delete from factoids where key=?',(str(tmp[0]),))
		self.c.execute('insert into factoids values (?,?,?,?)',(tmp[0],tmp[1],nick,time.time()))
	def del_factoid(self,query):
		self.c.execute('delete from factoids where key=?',(str(query),))
	def write_dict(self):
		dict.commit()
	def read_dict(self):
		self.c=dict.cursor()
		self.c.execute('''create table if not exists factoids (key, value, "by", ts)''')
		dict.commit()
	def query_dict(self,query):
		'''Primarily for the unittester	'''
		self.c=dict.cursor()
		self.c.execute('''select * from factoids where key=?''',(query,))
		results=self.c.fetchall()
		if len(results)>0:
			return results[0][1]
	def query(self,query,nick,channel):
		'''Querys the database for the factoid 'query', and returns its value to the channel if it is found'''
		self.c.execute('''select * from factoids where key=?''',(query.lower(),))
		results=self.c.fetchall()[:]
		if len(results)>0:
			self.msg(channel,str(results[0][1]).replace('%n',nick))
#		else:
#			self.send_infobot_query(query,nick,channel)
	#////////Single Functions/////////
	def hit(self,nick,data,channel):
		'''Causes BBot to punch someone'''
		who=data[data.find('hit ')+4:]
		self.msg(channel,'\x01ACTION punches %s\x01'%who)
	def version(self,nick,data,channel):
		'''Sends the version number to the channel'''
		self.msg(channel,'I am version %s'%BBot.version)
	def goog(self,nick,data,channel):
		if 'goog ' in data:
			w=str(data[data.find('goog ')+5:].replace(' ','+'))
			self.msg(channel,self.goog_str%w)
		return 0
	def wiki(self,nick,data,channel):
		w=data[data.find('wiki ')+5:].replace(' ','_')
		self.msg(channel,self.wiki_str%w)
		return 0
	def kb(self,nick,data,channel):
		w=data[data.find('kb ')+3:]
		self.msg(channel,self.kb_str%w)
		return 0
	def su_join(self,nick,data,channel):
		'''Makes BBot join the channel which is the param'''
		self.raw('JOIN %s'%data[data.find('join ')+5:])
	def su_writedb(self,nick,data,channel):
		'''Writes the factoids database to the harddrive'''
		dict.commit()
		self.notice(channel,'<<Wrote Database>>')
	def su_raw(self,nick,data,channel):
		self.raw(data[data.find('raw ')+4:])
	def su_part(self,nick,data,channel):
		self.raw('PART %s'%data[data.find('part ')+5:])
	def su_add(self,nick,data,channel):
		query=data[data.find(' :')+2:]
		query=query[query.find('add ')+4:].split(':::')
		self.add_factoid(query,nick)
		self.notice(channel,'<<Added %s>>'%query)
	def su_load(self,nick,data,channel):
		self.q=data[data.find('load ')+5:]
		if BBot.load_module(self.q,self.__server__):
			self.notice('#spam','<<Loaded %s>>'%self.q)
	def su_py(self,nick,data,channel):
		self.q=data[data.find('py ')+3:]
		try:
			ret=str(eval(self.q))
		except Exception,e:
			ret='<<Error %s; %s>>'%(type(e),e.args)
		self.msg(channel,ret)
	def su_connect(self,nick,data,channel):
		tmp=data[data.find('connect ')+8:]
		self.notice(channel,'<<Connecting to %s>>'%tmp)
		BBot.add_network(tmp)
		q.connections[tmp]=q.connection(tmp)
	def su_reload(self,nick,data,channel):
		tmp=data[data.find('reload ')+7:]
		BBot.reload_module(tmp,self.__server__)
		self.notice(channel,'<<Reloaded %s>>'%tmp)
	def su_del(self,nick,data,channel):
		tmp=data[data.find('del ')+4:]
		self.del_factoid(tmp)
		self.notice(channel,'<<Delete %s>>'%tmp)
