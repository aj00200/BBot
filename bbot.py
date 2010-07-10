#! /usr/bin/python
#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='2'
#Scan for open proxies on join? 1=yes,0=no. Requires nmap and python-namp: http://nmap.org  http://xael.org/norman/python/python-nmap/
import config

import socket
import sys
import re
import time
#import sqlite3
from random import randint
import thread
import api#BBot API Functions
import blockbotlib #some functions required for BlockBot(). Delete this like if you remove BlockBot()
import q
sys.path.insert(0,'%s/modules'%sys.path[0])
import bbot
import mathbot
import searchbot
import trekbot
import blockbot
import statusbot
def getHost(data):
	host=data[data.find('@')+1:data.find('PRIVMSG')]
	return host
def checkIfSuperUser(data,superusers):
	host=getHost(data)
	for su in superusers:
		if host.find(su)!=-1:
			return True
	else:
		return False
#===============HANDLERS=====
bb=blockbot.blockbot()
tb=trekbot.trekbot()
handlers=[bb,tb,bbot.bbot(),mathbot.mathbot(),searchbot.searchbot(),statusbot.statusbot()]#Run on msg
jhandlers=[bb,tb]#Run on Join
lhandlers=[]#Run every loop
nhandlers=[bb]
codes=[]#wb
continuepgm=1
def PONG(data):
	if data.find ('PING')!=-1:
		print('PING RECEIVED')
		irc.send('PONG '+data.split()[ 1 ]+'\r\n') #Return the PING to the server
		print('PONGING')
irc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
irc.connect((config.network,config.port))
print 'NICK'
irc.send('NICK %s\r\n'%config.mynick)
irc.send ('USER '+config.mynick+' '+config.mynick+' '+config.mynick+' :'+config.mynick+'\r\n')
needping=1
while needping:
	data=irc.recv(1024)
	if data.find('PING')!=-1:
		PONG(data)
		time.sleep(0.2)
		print 'IDENTIFY'
		irc.send('PRIVMSG NickServ :IDENTIFY '+config.username+' '+config.password+'\r\n')
		needping=0
		print(data)
time.sleep(config.sleep_after_join)
print('JOIN')
for each in config.autojoin:
	irc.send('JOIN '+each+'\r\n')
while continuepgm:
	data = irc.recv (config.wait_recv)
	print(data)
	PONG(data)
	if data.find('INVITE '+config.mynick+' :#')!=-1:
		newchannel=data.split(config.mynick+' :')[-1]
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
	elif re.search('[0-9]+ '+config.mynick,data):
		code=data.split()[1]
		for each in codes:
			each.code(code,data)
	if data.strip('\r\n')=='':
		continuepgm=0
	for handler in lhandlers:
		handler.loop()
	if q.queue.get_length():
		send=q.queue.pop()
		print(send)
		irc.send(send+'\r\n')
irc.send('QUIT :Quit: BBot Rulez\r\n')
