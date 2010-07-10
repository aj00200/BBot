#! /usr/bin/python
#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='1.7'
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
cline=config.readline()
port=int(cline.split('port: ')[-1].strip())
print('Connecting to: %s' % network)

cline=config.readline()
autojoin=cline.split('channels: ')[-1].split(' ')
cline=config.readline()
superusers=cline.split('super-user: ')[-1].split(' ')

cline=config.readline()
sleep_after_join=float(cline.split('wait-after-identify: ')[-1].strip())
cline=config.readline()
wait_recv=int(cline[cline.find(' '):].strip('\r\n'))
cline=config.readline()
cmd_char=cline[cline.find(' '):].strip('\r\n')
config.close()
del config
del cline

import socket
import sys
import re
import time
#import sqlite3
from random import randint
import thread

import blockbotlib #some functions required for BlockBot(). Delete this like if you remove BlockBot()
import api #BBot API Functions
sys.path.append('%s/modules'%sys.path[0])
#from folderbot import *

class queue_class():
	def __init__(self):
		self.queue=[]
	def get_length(self):
		return len(self.queue)
	def append(self,data):
		self.queue.append('PRIVMSG '+data[0]+' :'+data[1])
	def pop(self):
		return self.queue.pop(0)
	def join(self, channel):
		self.queue.append('JOIN '+channel)
	def part(self, channel, message=''):
		self.queue.append('PART %s :%s'%(channel,message))
	def kick(self,nick,channel,message=''):
		self.queue.append('KICK %s %s :%s!'%(channel,nick,message))
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

#===============HANDLERS=====
bb=BlockBot()
tb=trekbot()
wb=WhoBot()
handlers=[bb,BBot(),statusbot(),searchbot(),tb,wb]#Run on msg
jhandlers=[tb,bb]#Run on Join
lhandlers=[]#Run every loop
nhandlers=[bb]
codes=[wb]
continuepgm=1
def PONG(data):
	if data.find ('PING')!=-1:
		irc.send('PONG '+data.split()[ 1 ]+'\r\n') #Return the PING to the server
		print('PONGING')
irc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
irc.connect((network,port))
print 'NICK'
irc.send('NICK %s\r\n'%mynick)
irc.send ('USER '+mynick+' '+mynick+' '+mynick+' :'+mynick+'\r\n')
needping=1
while needping:
	data=irc.recv(1024)
	if data.find('PING')!=-1:
		PONG(data)
		needping=0
		print(data)
time.sleep(0.1)
print 'IDENTIFY'
irc.send('PRIVMSG NickServ :IDENTIFY '+username+' '+password+'\r\n')
time.sleep(sleep_after_join)
print('JOIN')
for each in autojoin:
	irc.send('JOIN '+each+'\r\n')
while continuepgm:
	data = irc.recv (wait_recv)
	print(data)
	PONG(data)
	if data.find('INVITE '+mynick+' :#')!=-1:
		newchannel=data.split(mynick+' :')[-1]
		irc.send('JOIN '+newchannel+'\r\n')
		del newchannel
	elif re.search(':*!*NOTICE #*:',data):
		nick=data[1:data.find('!')]
		channel=data[data.find(' NOTICE ')+8:data.find(':')]
		words=data[data.find('NOTICE')+6:]
		words=words[words.find(':'):]
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
			for jhandler in jhandlers:
				jhandler.join(nick,channel,ip,user)
	elif re.search('[0-9]+ '+mynick,data):
		code=data.split()[1]
		for each in codes:
			each.code(code,data)
	if data.strip('\r\n')=='':
		continuepgm=0
	for handler in lhandlers:
		handler.loop()
	if queue.get_length():
		send=queue.pop()
		print(send)
		irc.send(send+'\r\n')
irc.send('QUIT :Quit: BBot Rulez\r\n')
