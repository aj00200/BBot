#Asynchat Backend for BBot
import socket,asynchat,asyncore,re,time
import bbot,config
connections={}
class Connection(asynchat.async_chat):
	re001=re.compile('\.* 001')
	reNOTICE=re.compile('!(.)+ NOTICE (.)+ :')
	def __init__(self,address,port,ssl):
		asynchat.async_chat.__init__(self)
		self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
		self.set_terminator('\r\n')
		self.__address__=address
		self.data=''
		self.connect((self.__address__,port))
		#Set Buffer Size

		self.modules=[]
		for module in config.modules:
			self.modules.append(getattr(__import__('modules.'+module),module).module(self.__address__))
	def handle_connect(self):
		print('* Connected')
		self.push('NICK %s\r\nUSER %s BBot BBot :%s\r\n'%(config.nick,'BBot','BBot Version 6.0.0b'))
	def get_data(self):
		r=self.data
		self.data=''
		return r
	def found_terminator(self):
		data=self.get_data()
		#Check Ignore RE
		print(data)
		if data[:4]=='PING':
			self.push('PONG %s\r\n'%data[5:])
		elif re.search(self.reNOTICE,data):
			nick=data[1:data.find('!')]
			channel=data[data.find('ICE')+4:data.find(' :')]
			for module in self.modules:
				module.get_notice(nick,data,channel)
		elif ' PRIVMSG ' in data:
			nick=data[1:data.find('!')]
			channel=data[data.find('MSG')+4:data.find(' :')]
			for module in self.modules:
				module.privmsg(nick,data,channel)
		elif ' JOIN :#' in data:
			nick=data.split('!')[0][1:]
			if nick.find('#')==-1:
				channel=data[data.find(' :#')+2:]
				host=data[data.find('@')+1:data.find(' JOIN ')]
				user1=data[data.find('!'):data.find('@')]
				user = user1.replace("!","")
				for module in self.modules:
					module.get_join(nick,user,host,channel)
		elif re.search(self.re001,data):
			self.push('PRIVMSG NickServ :IDENTIFY %s %s\r\n'%(config.username,config.password))
			time.sleep(config.sleep_after_id)
			for channel in config.autojoin:
				self.push('JOIN %s\r\n'%channel)
		elif re.search('[0-9]+ *'+config.nick,data):
			code=data.split()[1]
			for module in self.modules:
				module.get_raw('CODE',(code,data))		
	def collect_incoming_data(self,data):
		self.data+=data
def connect(address,port=6667,ssl=False):
	'''Connect to an IRC network
	address - The network address of the IRC network
	port - On optional argument that specifies the port to connect on
	ssl - A boolean argument specifying wether or not to use SSL, not supported by this backend at this time.'''
	connections[address]=Connection(address,port,ssl)
