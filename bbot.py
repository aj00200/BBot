#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='1.1'
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
	def part(self, channel, message=''):
		self.queue.append('PART %s :%s'%(channel,message))
	def __init__(self):
		self.queue=[]
	def kick(self,nick,channel,message=''):
		self.queue.append('KICK %s %s :%s!'%(channel,nick,message))
	def get_length(self):
		return len(self.queue)
	def voice(self,nick,channel):
		self.queue.append('MODE '+channel+' +v '+nick)
	def nick(self,nick):
		self.queue.append('NICK %s'%nick)
		mynick=nick[:]
	def notice(self,data):
		self.queue.append('NOTICE '+data[0]+' :'+data[1])
	def mode(self,nick,channel,mode):
		self.queue.append('MODE '+channel+' '+mode+' '+nick)
	def kill(self,nick,reason=''):#Must be IRCOP
		self.queue.append('KILL %s :%s' % (nick,reason))
	def kline(self,host,time,reason):#Must be IRCOP
		self.queue.append('KLINE %s %s :%s'%(host,time,reason))
	def raw(self,data):
		self.queue.append(data)
queue=queue_class()	
class BBot():
	#database=sqlite3.connect('newdatabase.sql')
	def go(self,nick,data,channel):
		host=data.split(' PRIVMSG')[0].split('@')[-1]
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
			elif data.find(':?source')!=-1:
				queue.append((channel,nick+': My source code is written in Python and can be found at: http://github.com/aj00200/BBot'))
			elif data.find(':?kick ')!=-1:
				words=data.split(':?kick ')[-1].strip('\r\n')
				if words.lower().find(mynick.lower())!=-1:
					words=nick
				queue.append((channel,u'\x01ACTION kicks %s\x01'%words))
			elif ldata.find(':?about')!=-1:
				queue.append((channel,nick+': Im a bot by aj00200. %s' % version))
			elif ldata.find(':?aj00200')!=-1:
				queue.append((channel,nick+': aj00200 is the bots creator. aj0020020@live.com. He knows all.'))
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
		self.repeatlimit=3
		self.repeat_time=2
		self.repeat_1word=4
		self.msglist=[]
		self.lastnot=('BBot',time.time(),'sdkljfls')
		self.wait=1.5
	def checkForRepeatSpam(self,nick,data,channel):
		pass
	def join(self,nick,channel,ip,user):
		if ip.find('/')!=-1:
			queue.mode(nick,channel,'+v')
		#user=user.replace('~','')
		webchat=(str(blockbotlib.hex2dec('0x'+str(user[1:3])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[3:5])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[5:7])))+'.'+str(blockbotlib.hex2dec('0x'+str(user[7:9]))))
		try:
			self.jlist[channel[1:]].append(nick)
		except:
			print 'Err! Making channel var'
			self.jlist[channel[1:]]=[]
		#print 'in JOIN, scan DONE... Running...'
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
			elif ldata.find(':?ekill')!=-1:
				irc.send('QUIT')
				continuepgm=0
			elif ldata.find(':?protect')!=-1:
				queue.mode('',channel,'+mz')
			elif ldata.find(':?kl')!=-1:
				times=1
				if data.find('?kl ')!=-1:
					t=ldata.split('?kl ')[-1][0:-2]
					t=int(times)
					try:
						for each in range(t):
							queue.kick(self.jlist[channel[1:]].pop(),channel)
					except:
						queue.append((nick,'Kicking that many people has caused an error!'))
			elif not self.superuser:
				self.checkforspam(nick,data,channel)
	def checkforspam(self,nick,data,channel):
		self.msglist.insert(0,(nick,time.time(),data))
		if len(self.msglist)>5:
			self.msglist.pop()
		ident=data.split(' PRIVMSG ')[0].split('@')[0][1:]
		ldata=data.lower()
		for each in self.findlist:
			if ldata.find(each)!=-1:
				queue.kick(nick,channel)
		try:
			if self.msglist[0][0]==self.msglist[1][0]==self.msglist[2][0]:
				if (self.msglist[0][1]-self.msglist[2][1])<self.wait:
					queue.kick(nick,channel,'No Flooding!')
				if (self.msglist[0][2]==self.msglist[1][2]) and (self.msglist[0][1]-self.msglist[1][1]<self.repeat_time):
						queue.kick(nick,channel,'Please do not repeat!')
		except IndexError:
			pass
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
class trekbot():
	def go(self,nick,data,channel):
		ldata=data.lower()
		self.superuser=api.checkIfSuperUser(data,superusers)
		if self.superuser:
			if ldata.find('?op')!=-1:
				if ldata.find('?op ')!=-1:
					nick=ldata[ldata.find('?op')+4:].strip('\r\n')
				queue.mode(nick,channel,'+o')
			if ldata.find('?deop')!=-1:
				if ldata.find('?deop ')!=-1:
					nick=ldata[ldata.find('?deop ')+6:].strip('\r\n')
				queue.mode(nick,channel,'-o')
			if ldata.find('?voice')!=-1:
				if ldata.find('?voice ')!=-1:
					nick=ldata[ldata.find('?voice ')+7:].strip('\r\n')
				queue.mode(nick,channel,'+v')
			if ldata.find('?devoice')!=-1:
				if ldata.find('?devoice ')!=-1:
					nick=ldata[ldata.find('?devoice ')+9:].strip('\r\n')
				queue.mode(nick,channel,'-v')
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
class searchbot():
	def __init__(self):
		self.goog='http://www.google.com/search?q=%s'
		self.wiki='http://www.en.wikipedia.org/wiki/%s'
		self.pb='http://www.pastebin.com/%s'
		self.upb='http://paste.ubuntu.com/%s'
	def go(self,nick,data,channel):
		if data.find(':?goog ')!=-1:
			w=data.split(':?goog ')[-1].replace(' ','+')
			queue.append((channel,self.goog%w))
		elif data.find(':?wiki ')!=-1:
			w=data.split(':?wiki ')[-1].replace(' ','+')
			queue.append((channel,self.wiki%w))
		elif data.find(':?pb ')!=-1:
			w=data.split(':?pb ')[-1]
			queue.append((channel,self.pb%w))
		elif data.find(':?upb ')!=-1:
			w=data.split(':?upb ')[-1]
			queue.append((channel,self.upb%w))

#===============HANDLERS=====
bb=BlockBot()
handlers=[bb,BBot(),statusbot(),searchbot(),trekbot()]#Run on msg
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
print 'NICK'
irc.send('NICK '+mynick+'\r\n')
irc.send ( 'USER '+mynick+' '+mynick+' '+mynick+' :'+mynick+'\r\n' )
needping=1
ts=time.time()
while needping:
	data=irc.recv(512)
	if data.find('PING')!=-1:
		PONG(data)
		print 'IDENTIFY'
		irc.send('PRIVMSG NickServ :IDENTIFY '+username+' '+password+'\r\n')
		needping=0
	print data
	if time.time()-ts>5:
		needpin=0
time.sleep(sleep_after_join)

print 'JOIN'
for each in autojoin:
	irc.send('JOIN '+each+'\r\n')
while continuepgm:
	data = irc.recv ( 4096 )
	print(data)
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
	elif data.find(' PRIVMSG ')!=-1:
		channel=data.split(' PRIVMSG ')[1]
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
irc.send('QUIT :BBot Rulez\r\n')
