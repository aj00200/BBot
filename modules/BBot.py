import q
import api
import re
import config
import bbot as BBot
class bbot(api.module):
	def __init__(self,server):
		self.read_dict()
		self.q=''
		self.goog='http://www.google.com/search?q=%s'
		self.wiki='http://www.en.wikipedia.org/wiki/%s'
		self.pb='http://www.pastebin.com/%s'
		self.upb='http://paste.ubuntu.com/%s'
		self.kb='http://www.kb.aj00200.heliohost.org/index.py?q=%s'
		api.module.__init__(self,server)
	#database=sqlite3.connect('newdatabase.sql')
	def go(self,nick,data,channel):
		if channel.find('#')==-1:#Detect if the message is a PM to the Bot
			channel=nick.lower()
		ldata=data.lower()
		if api.checkIfSuperUser(data,config.superusers):
			if ldata.find('raw ')!=-1:
				self.raw(data.split('raw ')[-1])
			elif ldata.find('leave')!=-1:
				words=ldata.split('leave ')
				self.raw('PART %s' % words)
			elif data.find(':?add ')!=-1:
				self.q=data[ldata.find('?add ')+5:].strip('\r\n')
				self.q=self.q.split(':::')
				self.add_factoid(self.q)
			elif data.find(':?del ')!=-1:
				self.q=data[data.find('?del ')+5:].strip('\r\n')
				del self.static[self.q]
			elif ldata.find(':?writedict')!=-1:
				self.write_dict()
			elif ldata.find(':?connect ')!=-1:
				self.q=str(ldata[ldata.find(':?connect ')+10:].strip('\r\n'))
				self.append((channel,'Connecting to "%s"'%self.q))
				BBot.add_network(self.q)
				q.connections[self.q]=q.connection(self.q)
			elif ldata.find(':?load ')!=-1:
				self.q=ldata[ldata.find('?load ')+6:].strip('\r\n')
				BBot.load_module(str(self.q),str(self.__server__))
			elif data.find(':?py ')!=-1:
				self.q=data[data.find('?py ')+4:].strip('\r\n')
				try:
					ret=str(eval(self.q))
				except Exception,e:
					ret='Error: %s; Args: %s'%(type(e),e.args)
				self.append((channel,ret))
		if ldata.find(':'+config.mynick.lower()+': ')!=-1:
			self.q=ldata[ldata.find(':'+config.mynick.lower()+': ')+3+len(config.mynick):].strip('\r\n')
			if self.q in self.static:
				self.append((channel,self.static[self.q]))
		if re.search('(what|who|where) (is|was|are|am) ',ldata):
			self.ldata=ldata.replace(' was ',' is ')
			self.ldata=self.ldata.replace(' a ',' ')
			self.ldata=self.ldata.replace(' the ',' ')
			self.ldata=self.ldata.replace(' was ',' ')
			self.ldata=self.ldata.replace(' an ',' ')
			self.ldata=self.ldata.replace(' are ',' is ')
			self.ldata=self.ldata.replace(' am ',' is ')
			self.q=self.ldata[self.ldata.find(' is ')+4:].strip('?.\r\n:')
			if self.q in self.static:
				self.append((channel,nick+': '+self.static[self.q]))
		if data.find(':?')!=-1:
			if data.find(':?goog ')!=-1:
				w=data.split(':?goog ')[-1].replace(' ','+')
				self.append((channel,self.goog%w))
			elif data.find(':?wiki ')!=-1:
				w=data.split(':?wiki ')[-1].replace(' ','_')
				self.append((channel,self.wiki%w))
			elif data.find(':?pb ')!=-1:
				w=data.split(':?pb ')[-1]
				self.append((channel,self.pb%w))
			elif data.find(':?upb ')!=-1:
				w=data.split(':?upb ')[-1]
				self.append((channel,self.upb%w))
			elif data.find(':?kb ')!=-1:
				w=data[data.find(':?kb ')+5:]
				self.append((channel,self.kb%w))

			self.q=ldata[data.find(':?')+2:].strip('\r\n')
			if ' | ' in self.q:
				nick=self.q.split(' | ')
				self.q=nick[0]
				nick=nick[1]
			if ' > ' in self.q:
				self.nick=self.q.split(' > ')
				self.q=self.nick[0]
				channel=self.nick[1]
				nick='From %s'%nick
			if self.q in self.static:
				self.append((channel,nick+': '+self.static[self.q]))
			elif data.find(':?hit ')!=-1:
				words=data.split(':?hit ')[-1].strip('\r\n')
				if words.lower().find(config.mynick.lower())!=-1 or words.lower()=='aj00200':
					words=nick
				self.append((channel,'\x01ACTION kicks %s\x01'%words))
			elif data.find(':?version')!=-1:
				self.append((channel,'I am version %s.'%BBot.version))
	def add_factoid(self,query):
		self.static[query[0].lower()]=query[1]
	def del_factoid(self,query):
		if query in self.static:
			del self.static[query]
	def write_dict(self):
		self.dict=open('bbot/dict','w')
		for each in self.static:
			self.dict.write('%s:::%s\r\n'%(each,self.static[each]))
		self.dict.close()
	def read_dict(self):
		self.static={}
		self.dict=open('bbot/dict','r')
		for line in self.dict.readlines():
			self.q=line.strip('\r\n').split(':::')
			self.static[self.q[0]]=self.q[1]
		self.dict.close()
	def query_dict(self,query):
		'''
		Primarily for the unittester
		'''
		if query in self.static:
			return self.static[query]
module=bbot
