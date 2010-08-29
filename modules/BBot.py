import q
import api
import re
import config
import bbot as BBot
import time
import thread
dict={}
class bbot(api.module):
	commands=['help','goog','wiki','pb','upb','kb','hit','?<query>','add','del','writedict','load','reload','py','connect']
	def get_command_list(self):
		try:
			time.sleep(3)
			for module in BBot.networks[self.__server__]:
				for command in module.commands:
					self.command_list.append(command)
		except Exception,e:
			print 'Error: %s; with args: %s;'%(type(e),e.args)
	def __init__(self,server):
		thread.start_new_thread(self.get_command_list,())
		self.read_dict()
		self.info_bots=['gpy','aj00200','BBot','JCSMarlen']
		self.q=''
		self.command_list=[]
		self.goog='http://www.google.com/search?q=%s'
		self.wiki='http://www.en.wikipedia.org/wiki/%s'
		self.pb='http://www.pastebin.com/%s'
		self.upb='http://paste.ubuntu.com/%s'
		self.kb='http://www.kb.aj00200.heliohost.org/index.py?q=%s'
		api.module.__init__(self,server)
	def go(self,nick,data,channel):
		if channel.find('#')==-1:#Detect if the message is a PM to the Bot
			channel=nick.lower()
		ldata=data.lower()
		if api.checkIfSuperUser(data,config.superusers):
			if ldata.find('raw ')!=-1:
				self.raw(data.split('raw ')[-1])
				return 0 #Just for speed
			elif ldata.find('leave')!=-1:
				words=ldata.split('leave ')
				self.raw('PART %s' % words)
				return 0
			elif data.find(':?add ')!=-1:
				self.q=data[ldata.find('?add ')+5:].strip('\r\n')
				self.q=self.q.split(':::')
				self.add_factoid(self.q)
				return 0
			elif data.find(':?del ')!=-1:
				self.q=data[data.find('?del ')+5:].strip('\r\n')
				self.del_factoid(self.q)
				return 0
			elif ldata.find(':?writedict')!=-1:
				self.write_dict()
				return 0
			elif ldata.find(':?connect ')!=-1:
				self.q=str(ldata[ldata.find(':?connect ')+10:].strip('\r\n'))
				self.append((channel,'Connecting to "%s"'%self.q))
				BBot.add_network(self.q)
				q.connections[self.q]=q.connection(self.q)
				return 0
			elif ldata.find(':?load ')!=-1:
				self.q=ldata[ldata.find('?load ')+6:].strip('\r\n')
				BBot.load_module(str(self.q),str(self.__server__))
				return 0
			elif data.find(':?py ')!=-1:
				self.q=data[data.find('?py ')+4:].strip('\r\n')
				try:
					ret=str(eval(self.q))
				except Exception,e:
					ret='Error: %s; Args: %s'%(type(e),e.args)
				self.append((channel,ret))
				return 0
			elif data.find(':?reload ')!=-1:
				self.q=data[data.find(':?reload ')+9:].strip('\r\n')
				BBot.reload_module(self.q,str(self.__server__))
				return 0
		if ldata.find(':'+config.mynick.lower()+': ')!=-1:
			self.q=ldata[ldata.find(':'+config.mynick.lower()+': ')+3+len(config.mynick):].strip('\r\n')
			if self.q in dict:
				self.append((channel,dict[self.q]))
			else:
				self.infobot_query(self.q,nick)
			return 0
		if re.search('(what|who|where) (is|was|are|am) ',ldata):
			self.ldata=ldata.replace(' was ',' is ')
			self.ldata=self.ldata.replace(' a ',' ')
			self.ldata=self.ldata.replace(' the ',' ')
			self.ldata=self.ldata.replace(' was ',' ')
			self.ldata=self.ldata.replace(' an ',' ')
			self.ldata=self.ldata.replace(' are ',' is ')
			self.ldata=self.ldata.replace(' am ',' is ')
			self.q=self.ldata[self.ldata.find(' is ')+4:].strip('?.\r\n:')
			if self.q in dict:
				self.append((channel,nick+': '+dict[self.q]))
			else:
				self.infobot_query(self.q,nick)
			return 0
		if data.find(':?')!=-1:
			if ':?help' in data and ':?help ' not in data:
				w=''
				for cmd in self.command_list:
					w+='%s, '%cmd
				self.append((channel,'%s: %s'%(nick,w[0:-2])))
			if ':?goog ' in data:
				w=data.split(':?goog ')[-1].replace(' ','+')
				self.append((channel,self.goog%w))
				return 0
			elif ':?wiki ' in data:
				w=data.split(':?wiki ')[-1].replace(' ','_')
				self.append((channel,self.wiki%w))
				return 0
			elif ':?pb ' in data:
				w=data.split(':?pb ')[-1]
				self.append((channel,self.pb%w))
				return 0
			elif ':?upb ' in data:
				w=data.split(':?upb ')[-1]
				self.append((channel,self.upb%w))
				return 0
			elif ':?kb 'in data:
				w=data[data.find(':?kb ')+5:]
				self.append((channel,self.kb%w))
				return 0
			elif ':?hit ' in data:
				words=data[data.find(':?hit ')+6:]
				if words.lower().find(config.mynick.lower())!=-1 or words.lower()=='aj00200':
					words=nick
				self.append((channel,'\x01ACTION kicks %s\x01'%words))
				return 0
			elif ':?version' in data:
				self.append((channel,'I am version %s.'%BBot.version))
				return 0
			self.q=ldata[data.find(':?')+2:].strip('\r\n')
			if ' > ' in self.q:
				if ' | ' not in self.q:
					self.nick=self.q.split(' > ')
					self.q=self.nick[0]
					channel=self.nick[1]
					nick='From %s'%nick
				else:
					self.append((channel,nick+': All abuse is logged: %s'%data))
					return 1
			elif ' | ' in self.q:
				nick=self.q.split(' | ')
				self.q=nick[0]
				nick=nick[1]
			if self.q[:self.q.find(' ')] not in self.command_list:
				if self.q in dict:
					self.append((channel,nick+': '+dict[self.q]))
					return 0
				else:
					self.infobot_query(self.q,nick)
		elif ':INFOBOT:' in data:
			if ':INFOBOT:REPLY' in data:
				if nick in self.info_bots:
					self.infobot_parse_reply(data)
			elif ':INFOBOT:QUERY' in data:
				self.infobot_reply(data,nick)
	def infobot_query(self,query,nick):
		for each in self.info_bots:
			self.append((each,'INFOBOT:QUERY %s %s'%(nick,query)))
	def infobot_parse_reply(self,query):
		print 'PARSING REPLY'
		q=query[query.find('INFOBOT:REPLY ')+14:]
		q=q[q.find(' ')+1:].replace('<ACTION>','\x01ACTION')
		if '\x01' in q:
			q+='\x01'
		print 'ADDING FACTOID %s'%q.split(' = ')
		self.add_factoid(q.split(' = ',1))
	def infobot_reply(self,query,sender):
		try:
			q=query[query.find('INFOBOT:QUERY ')+14:]
			nick=q[:q.find(' ')]
			self.q=q[q.find(' ')+1:]
			if self.q in dict:
				self.append((sender,'INFOBOT:REPLY %s %s = %s'%(nick,self.q,dict[self.q])))
			else:
				self.append((sender,'INFOBOT:DUNNO %s %s'%(nick,self.q)))
		except Exception,e:
			self.append((channel,'Error %s; with args %s;'%(type(e),e.args)))
	def add_factoid(self,query):
		dict[query[0].lower()]=query[1]
	def del_factoid(self,query):
		if query in dict:
			del dict[query]
	def write_dict(self):
		self.dict=open('bbot/dict','w')
		for each in dict:
			self.dict.write('%s:::%s\r\n'%(each,dict[each]))
		self.dict.close()
	def clear_dict(self):
		dict={}
	def read_dict(self):
		self.clear_dict()
		self.dict=open('bbot/dict','r')
		for line in self.dict.readlines():
			self.q=line.strip('\r\n').split(':::')
			dict[self.q[0]]=self.q[1]
		self.dict.close()
	def query_dict(self,query):
		'''
		Primarily for the unittester
		'''
		if query in dict:
			return dict[query]
module=bbot
