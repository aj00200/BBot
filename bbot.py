#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
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
autojoin=cline.split('channels: ')[-1].split(' ')
port = 6667

import socket
import re
import time
import sqlite3
#import nmap
from random import randint

class que_class():
	def append(self,data):
		self.que.append('PRIVMSG '+data[0]+' :'+data[1])
	def pop(self):
		return self.que.pop()
	def join(self, channel):
		self.que.append('JOIN '+channel)
	def __init__(self):
		self.que=[]
		self.rque=[]
	def kick(self,nick,channel):
		self.que.append('KICK '+channel+' '+nick+' :BBot Rulez!')
	def get_length(self):
		return len(self.que)
	def voice(self,nick,channel):
		self.que.append('MODE '+channel+' +v '+nick)
	def nick(self,nick):
		self.que.append('NICK '+nick)
	def notice(self,data):
		self.que.append('NOTICE '+data[0]+' :'+data[1])
	def mode(self,nick,channel,mode):
		self.que.append('MODE '+channel+' '+mode+' '+nick)
que=que_class()	
class BBot:
	database=sqlite3.connect('newdatabase.sql')
	def go(self,nick,data,channel):
		ldata=data.lower()
		if re.search(':(bbot|BBot|Bbot): (hi|hello)[^a-zA-Z ]',ldata):
			print('HI')
			que.append((channel,'Hi '+nick+'!'))
		if data.find('?')!=-1:
			if data.find('?ping')!=-1:
				que.append((channel,'PONG'))
			elif data.find('?toast')!=-1:
				que.append((channel,'Your toast will be done soon :D'))
			elif data.find(':?source')!=-1:
				que.append((channel,nick+': My soruce code is written in Python and can be found at: http://github.com/aj00200/BBot'))
			elif data.find('?kick ')!=-1:
				words=data.split('?kick ')[-1]
				if words.lower().find('bbot')!=-1:
					words=nick
				que.append((channel,'BBot kicks '+words))
			elif ldata.find(':?about')!=-1:
				que.append((channel,nick+': Im a bot by aj00200. v0.9.0'))
			elif ldata.find(':?aj00200')!=-1:
				que.append((channel,nick+': aj00200 is the bots creator. aj0020020@live.com. He knows all.'))
			elif data.find(':?sqltest ')!=-1:
				print data.split('sqltest ')[-1]
				sqldata=BBot.database.cursor()
				sqldata.execute(data.split('sqltest ')[-1])
				for row in sqldata:
					print '* '+str(row)
					que.append((channel,str(row)))
			elif ldata.find(':?help')!=-1:
				if ldata.find(':?help ')!=-1:
					words=ldata.split(':?help ')[-1]
					if words.find('kick')!=-1:
						que.append((channel,'Makes BBot injure the person. *SYNTAX:* ?kick <nick>'))
					elif words.find('about')!=-1:
						que.append((channel,'Tells about BBot and its current version'))
					elif words.find('source')!=-1:
						que.append((channel,'Tells you where to find my source code. GNU GPL version 3 by the way...'))
					else:
						que.append((channel,'Sorry, that command does not exist'))
				else:
					que.append((channel,nick+': ?kick, ?about, ?help, ?source, ?aj00200, ?toast'))
			else:
				pass
class BlockBot():
	def join(self,nick,channel,ip,user):
		if ip.find('/')!=-1:
			que.mode(nick,channel,'+v')
		#user=user.replace('~','')
		webchat=(str(self.hex2dec('0x'+str(user[1:3])))+'.'+str(self.hex2dec('0x'+str(user[3:5])))+'.'+str(self.hex2dec('0x'+str(user[5:7])))+'.'+str(self.hex2dec('0x'+str(user[7:9]))))
		#que.append(('aj00200',nick+': '+webchat))
		#self.jlist[channel[1:]].append(nick)
		
		#self.scan(ip, channel, nick)
		#print 'in JOIN, scan DONE... Running...'
		#if self.safe:
		#	print (ip,channel,nick)
		#	print 'MODE '+channel+' +v '+nick+'\r\n'
		#	irc.send('MODE '+channel+' +v '+nick+'\r\n')
	def scan(self,ip,channel,nick):
		self.safe=1
		host=ip
	
		try:
			print('Scanning '+ip)
			nm=nmap.PortScanner()
			#80, 8080, 1080, 3246
			nm.scan(ip,'808,23,1080,110,29505,8080,3246','-T5')
			print 'Scan Done...'
			print '----------'
			for each in nm.all_hosts():
				print each+':::'
				lport = nm[each]['tcp'].keys()
				print lport
				if 808 in lport or 23 in lport or 110 in lport or 1080 in lport or 29505 in lport or 80 in lport or 8080 in lports or 3246 in lports:
					self.safe=0
					print 'DRONE'
	#		lport.sort()
	#		for port in lport:
	#		print 'port : %s\tstate : %s' % (port, nm[ip]['tcp'][port]['state'])
	#		if 'proxy' in nm[ip]['tcp'][port]['name'] or 'telnet' in nm[ip]['tcp'][port]['name']:
		#		if nm[ip]['tcp'][808]['state']==u'open' or nm[ip]['tcp'][23]['state']==u'open':
	#				print(ip+' is most likely a DRONE')
	#				self.safe=0
				#que.append((channel,'NOTICE: '+ip+' is most likely a drone!'))
			del nm
		except:
			print 'CRASH'
		#
	def dec2hex(self,n):
		return "%X" % n
	def hex2dec(self,s):
		try:
			return int(s, 16)
		except:
			return 'error'
	def go(self,nick,data,channel):
		ldata=data.lower()
		self.oolastmsg=(self.olastmsg[:])
		self.olastmsg=(self.lastmsg[:])
		self.lastmsg=(nick,time.time(),data)
		for each in self.findlist:
			if ldata.find(each)!=-1:
				que.kick(nick,channel)
		if self.olastmsg[0]==self.lastmsg[0]==self.oolastmsg[0]:
			if (self.lastmsg[1]-self.oolastmsg[1])<self.wait:
				que.kick(nick,channel)
		if data.find('network/')!=-1 or data.find('staff/')!=-1:
			print 'HI Staff/Developer'
			if ldata.find('?;')!=-1:
				self.findlist.append(data.split('?; ')[-1][0:-2])
			elif ldata.find('?faster')!=-1:
				print 'FASTER'
				self.wait=self.wait/2
			elif ldata.find('?slower')!=-1:
				print('SLOWER')
				self.wait=self.wait*2
			elif ldata.find('?setspeed ')!=-1:
				self.wait=int(data.split('?setspeed ')[-1][0:-2])
			elif ldata.find('?rehash')!=-1:
				self.__init__()
			elif ldata.find('?protect')!=-1:
				que.mode('',channel,'+mz')
			elif ldata.find('?kl')!=-1:
				times=1
				if data.find('?kl ')!=-1:
					times=ldata.split('?kl ')[-1][0:-2]
					times=int(times)
					print 'times: '+times
				try:
					for each in range(0,times):
						que.kick(self.jlist.pop())
				except:
					pass
	def notice(self,nick,channel,data):
		print time.time()
		ldata=data.lower()
		self.olastnot=(self.lastnot[0:])
		self.lastnot=(nick,time.time())
		if self.olastnot[0]==self.lastnot[0]:
			if (self.lastnot[1]-self.olastnot[1])<self.wait:
				que.kick(nick,channel)
		for each in self.findlist:
			if ldata.find(each)!=-1:
				que.kick(nick,channel)
	def __init__(self):
		self.jlist={}
		self.findlist=['for all your irc needs','gnaa','bycycle computers he','i can never be klined','autistic status','dubkat here,']
		self.lastmsg=('BBot',time.time(),'hi')
		self.lastnot=('BBot',time.time(),'sdkljfls')
		self.olastmsg=('BBot',time.time(),'clear')
		self.wait=1.5
	def nicklist(self,channel,data):
		words=data.split(mynick)[-1]
class Ubuntu():
	def go(self,nick,data,channel):
		ldata=data.lower()
		if data.find(' | '):
			self.to=1
			self.name=data.split(' | ')[-1]
			self.actor=data.split(' | ')[0]
		else:
			self.actor=ldata
	#===HELP===
		if ldata.find(':!u help')!=-1:
			que.append((nick,': !u samba'))
	#===REGULAR===
		if ldata.find(':!u smb')!=-1 or ldata.find(':!u samba')!=-1:
			self.msg='Samba (https://help.ubuntu.com/9.10/serverguide/C/windows-networking.html) is a program that allows file and printer sharing between Ubuntu and Windows.'
			if self.to==1:
				que.append((channel,self.name+': '+self.msg))
			if self.to==2:
				que.send((self.name,self.msg))
			else:
				que.append((channel,self.msg))
#		elif data.
class Firefox():
	def go(self,nick,data,channel):
		msgtype=0
		if data.find(' | '):
			msgtype=1
		if data.find(':?f ')!=-1:
			words=data.split('?f ')[-1][0:-2]
			if words.find('download')!=-1:
				self.send(nick,channel,msgtype,'You can download Firefox at: www.firefox.com')
	def send(self,nick,channel,type,data):
		if type==0:
			que.append((channel, nick+': '+data))
		
#===============HANDLERS=====
bb=BlockBot()
handlers=[bb,BBot(),Firefox()]#Run on msg
#handlers=[]
jhandlers=[bb]#Run on Join
#jhandlers=[]
lhandlers=[]#Run every loop
#nhandlers=[BlockBot()]#run on notice
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
needping=1
print 'USER'
irc.send ( 'USER BBot BBot BBot :BBot\r\n' )
while needping:
	data=irc.recv(4096)
#	ndata=data.split('\r\n')
#	for each in ndata:
#		que.radd(each)
#	data=que.read()
	if data.find('PING')!=-1:
		PONG(data)
		print 'IDENTIFY'
		irc.send('PRIVMSG NickServ :IDENTIFY '+username+' '+password+'\r\n')
		needping=0
	print data
time.sleep(1.7)
data = irc.recv ( 4096 )
PONG(data)
print 'JOIN'
for each in autojoin:
	irc.send('JOIN '+each+'\r\n')
while continuepgm:
	data = irc.recv ( 4096 )
	if data.find('!kill')!=-1:
		continuepgm=0
	elif data.find ( 'PING' ) != -1:
#		irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' ) #Return the PING to the server
		PONG(data)

		print('PONGING')


	elif data.find('INVITE '+mynick+' :#')!=-1:
		newchannel=data.split(mynick+' :')[-1]
		irc.send('JOIN '+newchannel+'\r\n')
		del newchannel

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
			print 'IP found was :'+ip
			for jhandler in jhandlers:
				jhandler.join(nick, channel, ip, user)
		else:
			irc.send('MODE '+channel+' +v '+nick+'\r\n')
	elif data.find(' NOTICE ')!=-1:
		nick=data.split('!')[0][1:]
		channel=data.split(' NOTICE ')[1].split(' :')[0]
		words=data.split('NOTICE')[1].split(':')[1]
		for handler in nhandlers:
			handler.notice(nick,channel,words)
	for handler in lhandlers:
		handler.loop()
	if que.get_length()>0:
		send=que.pop()
		irc.send(send+'\r\n')
	print data
irc.send('QUIT :BBot Rulez\r\n')
