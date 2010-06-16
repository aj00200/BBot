#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='v0.96'
proxyscan=1#Scan for open proxies on join? 1=yes,0=no. Requires nmap and python-namp: http://nmap.org  http://xael.org/norman/python/python-nmap/
globals=[]
config=open('config','r')
cline=config.readline()
mynick=cline.split('nick: ')[-1][0:-1]
cline=config.readline()
username=cline.split('username: ')[-1][0:-1]
cline=config.readline()
password=cline.split('password: ')[-1][0:-1]
cline=config.readline()
network=cline.split('network: ')[-1][0:-1]
print('Connecting to: %s' % network)
cline=config.readline()
port=int(cline.split('port: ')[-1].strip())
cline=config.readline()
autojoin=cline.split('channels: ')[-1].split(' ')
cline=config.readline()
superusers=cline.split('super-user: ')[-1].split(' ')
cline=config.readline()
sleep_after_join=float(cline.split('wait-after-identify: ')[-1].strip())
config.close()
del config
del cline

import socket
import re
import time
import sqlite3
from random import randint
import urllib
import thread
import blockbotlib#some functions required for BlockBot(). Delete this like if you remove BlockBot()
import api#BBot API Functions

class queue_class():
	def append(self,data):
		self.queue.append('PRIVMSG '+data[0]+' :'+data[1])
	def pop(self):
		return self.queue.pop()
	def join(self, channel):
		self.queue.append('JOIN '+channel)
	def __init__(self):
		self.queue=[]
		self.rqueue=[]
	def kick(self,nick,channel):
		self.queue.append('KICK '+channel+' '+nick+' :BBot Rulez!')
	def get_length(self):
		return len(self.queue)
	def voice(self,nick,channel):
		self.queue.append('MODE '+channel+' +v '+nick)
	def nick(self,nick):
		self.queue.append('NICK '+nick)
	def notice(self,data):
		self.queue.append('NOTICE '+data[0]+' :'+data[1])
	def mode(self,nick,channel,mode):
		self.queue.append('MODE '+channel+' '+mode+' '+nick)
	def kill(self,nick,reason=''):#Must be IRCOP
		self.queue.append('KILL %s :%s' % (nick,reason))
	def kline(self,host,time,reason):#Must be IRCOP
		self.queue.append('KLINE %s %s :%s'%(host,time,reason))
queue=queue_class()	
class BBot():
	#database=sqlite3.connect('newdatabase.sql')
	def go(self,nick,data,channel):
		host=data.split(' PRIVMSG')[0].split('@')[-1]
		print host
		if channel.find('#')==-1:
			channel=nick.lower()
		ldata=data.lower()
		for su in superusers:
			if host.find(su)!=-1:
				if ldata.find('raw ')!=-1:
					irc.send(data.split('raw ')[-1])
				elif ldata.find('leave')!=-1:
					words=ldata.split('leave ')
					irc.send('PART %s' % words)
		if re.search(':'+mynick.lower()+'(:|,) (hi|hello)[^a-zA-Z ]',ldata):
			print('HI')
			queue.append((channel,'Hi '+nick+'!'))
		if data.find('?')!=-1:
			if data.find(':?ping')!=-1:
				queue.append((channel,'PONG'))
			elif data.find(':?goog ')!=-1:
				words=data.split(':?goog ')[-1]
				queue.append((channel,'http://www.google.com/search?q=%s' % words))
			elif data.find(':?toast')!=-1:
				queue.append((channel,'Your toast will be done soon :D'))
			elif data.find(':?source')!=-1:
				queue.append((channel,nick+': My source code is written in Python and can be found at: http://github.com/aj00200/BBot'))
			elif data.find(':?kick ')!=-1:
				words=data.split(':?kick ')[-1]
				if words.lower().find(mynick.lower())!=-1:
					words=nick
				queue.append((channel,u'\x01ACTION kicks %s\x01'%words))
			elif ldata.find(':?about')!=-1:
				queue.append((channel,nick+': Im a bot by aj00200. %s' % version))
			elif ldata.find(':?aj00200')!=-1:
				queue.append((channel,nick+': aj00200 is the bots creator. aj0020020@live.com. He knows all.'))
			elif data.find(':?sqltest ')!=-1:
				print data.split(':sqltest ')[-1]
				sqldata=BBot.database.cursor()
				sqldata.execute(data.split('sqltest ')[-1])
				for row in sqldata:
					print '* '+str(row)
					queue.append((channel,str(row)))
			elif ldata.find(':?help')!=-1:
				if ldata.find(':?help ')!=-1:
					words=ldata.split(':?help ')[-1]
					if words.find('kick')!=-1:
						queue.append((channel,'Makes BBot injure the person. *SYNTAX:* ?kick <nick>'))
					elif words.find('about')!=-1:
						queue.append((channel,'Tells about BBot and its current version'))
					elif words.find('source')!=-1:
						queue.append((channel,'Tells you where to find my source code. GNU GPL version 3 by the way...'))
					else:
						queue.append((channel,'Sorry, that command does not exist'))
				else:
					queue.append((channel,nick+': ?kick, ?about, ?help, ?source, ?aj00200, ?toast'))
			else:
				pass
class BlockBot():
	def __init__(self):
		self.ignore_users_on_su_list=1#Don't kick users if they are on the superusers list
		self.jlist={}
		self.config=open('blockbot-config','r')
		self.findlist=self.config.readline().split('spam-strings: ')[-1].split('#')[0].split('^^^@@@^^^')
		self.proxyscan=0
		if self.config.readline().lower().split('#')[0].find('yes')!=-1:
			self.proxyscan=1
			proxyscan=1
		if self.proxyscan==1:
			import nmap #Can be found at: http://xael.org/norman/python/python-nmap/
		self.lastmsg=('BBot',time.time(),'hi')
		self.lastnot=('BBot',time.time(),'sdkljfls')
		self.olastmsg=('BBot',time.time(),'clear')
		self.wait=1.5
	def nicklist(self,channel,data):
		words=data.split(mynick)[-1]
	def join(self,nick,channel,ip,user):
		if ip.find('/')!=-1:
			queue.mode(nick,channel,'+v')
		#user=user.replace('~','')
		webchat=(str(blockbotlib.hex2dec('0x'+str(user[1:3])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[3:5])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[5:7])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[7:9]))))
		#queue.append(('aj00200',nick+': '+webchat))
		#self.jlist[channel[1:]].append(nick)
		
		#self.scan(ip, channel, nick)
		#print 'in JOIN, scan DONE... Running...'
		#if self.safe:
		#	print (ip,channel,nick)
		#	print 'MODE '+channel+' +v '+nick+'\r\n'
		#	irc.send('MODE '+channel+' +v '+nick+'\r\n')
		if proxyscan:
			thread.start_new_thread(self.scan, (ip,channel,nick))
	def scan(self,ip,channel,nick):
		scansafe=1
		try:
			print('Scanning '+ip)
			nm=nmap.PortScanner()
			#80, 8080, 1080, 3246
			nm.scan(ip,'808,23,1080,110,29505,8080,3246','-T5')
			for each in nm.all_hosts():
				print each+':::'
				lport = nm[each]['tcp'].keys()
				print lport
				if 808 in lport or 23 in lport or 110 in lport or 1080 in lport or 29505 in lport or 80 in lport or 8080 in lports or 3246 in lports:
					scansafe=0
					print 'DRONE'
			#if 'proxy' in nm[ip]['tcp'][port]['name'] or 'telnet' in nm[ip]['tcp'][port]['name']:
			#	if nm[ip]['tcp'][808]['state']==u'open' or nm[ip]['tcp'][23]['state']==u'open':
			#		print(ip+' is most likely a DRONE')
			#		scansafe=0
				#queue.append((channel,'NOTICE: '+ip+' is most likely a drone!'))
			del nm
			if scansafe:
				queue.mode(nick,channel,'+v')
			print 'Scan Done...'
		except:
			print 'PYTHON NMAP CRASH'
	def go(self,nick,data,channel):
		ldata=data.lower()
		if self.ignore_users_on_su_list:
			self.superuser=api.checkIfSuperUser(data,superusers)
			print self.superuser
		if self.superuser:
			if ldata.find(':?;')!=-1:
				self.findlist.append(data.split(':?; ')[-1][0:-2])
			elif ldata.find(':?faster')!=-1:
				print 'FASTER'
				self.wait=self.wait/2
			elif ldata.find(':?slower')!=-1:
				print('SLOWER')
				self.wait=self.wait*2
			elif ldata.find(':?setspeed ')!=-1:
				self.wait=float(data.split('?setspeed ')[-1][0:-2])
			elif ldata.find(':?rehash')!=-1:
				self.__init__()
			elif ldata.find(':?protect')!=-1:
				queue.mode('',channel,'+mz')
			elif ldata.find('?:kl')!=-1:
				times=1
				if data.find('?kl ')!=-1:
					times=ldata.split('?kl ')[-1][0:-2]
					times=int(times)
					print 'times: '+times
				try:
					for each in range(0,times):
						queue.kick(self.jlist.pop())
				except:
					pass
		elif not self.superuser:
			self.checkforspam(nick,data,channel)
	def checkforspam(self,nick,data,channel):
		host=data.split(' PRIVMSG ')[0].split('@')[-1]
		ident=data.split(' PRIVMSG ')[0].split('@')[0][1:]
		ldata=data.lower()
		self.oolastmsg=(self.olastmsg[:])
		self.olastmsg=(self.lastmsg[:])
		self.lastmsg=(nick,time.time(),data[data.find(channel):])
		for each in self.findlist:
			if ldata.find(each)!=-1:
				queue.kick(nick,channel)
		if self.olastmsg[0]==self.lastmsg[0]==self.oolastmsg[0]:
			if (self.lastmsg[1]-self.oolastmsg[1])<self.wait:
				queue.kick(nick,channel)
		if (self.lastmsg[2]==self.olastmsg[2]) and (self.lastmsg[1]-self.olastmsg[1]<10):
			queue.kick(nick,channel)
			queue.kick(self.olastmsg[0],channel)

	def notice(self,nick,channel,data):
		print time.time()
		ldata=data.lower()
		self.olastnot=(self.lastnot[0:])
		self.lastnot=(nick,time.time())
		if self.olastnot[0]==self.lastnot[0]:
			if (self.lastnot[1]-self.olastnot[1])<self.wait:
				queue.kick(nick,channel)
		for each in self.findlist:
			if ldata.find(each)!=-1:
				queue.kick(nick,channel)

class statusbot():
	def __init__(self):
		self.statuses={}
	def go(self,nick,data,channel):
		if data.find(':?status ')!=-1:
			words=data.split('?status')[-1].strip('\r\n')
			self.statuses[nick]=words[:]
		elif data.find(':?whereis ')!=-1:
			try:
				words=data.split(':?whereis ')[-1].strip('\r\n')
				queue.append((channel,nick+': %s is: '%words+self.statuses[words]))
			except:
				queue.append((channel,nick+': %s hasn\'t left a status.'%words))
		elif data.find('?notify ')!=-1:
			words=data.split(':?notify ')[-1].strip('\r\n').strip('#')
			queue.append((words,'Just letting you know, %s is looking for you in %s' % (nick,channel)))
		elif data.find(':?reset')!=-1:
			words=data.split(':?reset')[-1].strip('\r\n')
			try:
				del self.statuses[words]
			except:
				pass
#===============HANDLERS=====
bb=BlockBot()
handlers=[bb,BBot(),statusbot()]#Run on msg
jhandlers=[bb]#Run on Join
lhandlers=[]#Run every loop
nhandlers=[bb]
continuepgm=1
def PONG(data):
	if data.find ( 'PING' ) != -1:
		irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' ) #Return the PING to the server
		print('PONGING')

irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
print 'NICK'
irc.send('NICK '+mynick+'\r\n')
irc.send ( 'USER '+mynick+' '+mynick+' '+mynick+' :'+mynick+'\r\n' )
needping=1
while needping:
	data=irc.recv(4096)
	if data.find('PING')!=-1:
		PONG(data)
		print 'IDENTIFY'
		irc.send('PRIVMSG NickServ :IDENTIFY '+username+' '+password+'\r\n')
		needping=0
	print data
time.sleep(sleep_after_join)

print 'JOIN'
for each in autojoin:
	irc.send('JOIN '+each+'\r\n')
while continuepgm:
	data = irc.recv ( 4096 )
	PONG(data)
	if data.find('INVITE '+mynick+' :#')!=-1:
		newchannel=data.split(mynick+' :')[-1]
		irc.send('JOIN '+newchannel+'\r\n')
		del newchannel
	elif data.find(' NOTICE ')!=-1:
		print data
		nick=data.split('!')[0][1:]
		channel=data.split(' NOTICE ')[1].split(' :')[0]
		words=data.split('NOTICE')[1].split(':')[1]
		for handler in nhandlers:
			handler.notice(nick,channel,words)
	elif data.find('PRIVMSG ')!=-1:
		channel=data.split('PRIVMSG ')[-1]
		channel=channel.split(' :')[0]
		nick=data.split('!')[0][1:]
		for handler in handlers:
			handler.go(nick,data,channel)
	elif data.find(' JOIN :#')!=-1:
		nick=data.split('!')[0][1:]
		if nick.find('#')==-1:
			channel='#'+data.split(' :#')[-1][0:-2]
			ip=data.split('@')[1].split(' JOIN')[0]
			user=data.split('@')[0].split('!')[-1]
			print('IP found was :'+ip)
			for jhandler in jhandlers:
				jhandler.join(nick, channel, ip, user)
		else:
			irc.send('MODE '+channel+' +v '+nick+'\r\n')

	for handler in lhandlers:
		handler.loop()
	if queue.get_length()>0:
		send=queue.pop()
		print(send)
		irc.send(send+'\r\n')
	print data
irc.send('QUIT :BBot Rulez\r\n')
