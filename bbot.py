#! /usr/bin/python
import q
#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='2'
#Scan for open proxies on join? 1=yes,0=no. Requires nmap and python-namp: http://nmap.org  http://xael.org/norman/python/python-nmap/

import config

#import socket
import sys
import re
import time
import thread
import api#BBot API Functions
import asyncore
sys.path.insert(0,'%s/modules'%sys.path[0])
import BBot
import mathbot
import searchbot
import trekbot
import blockbot
import statusbot
import rpgbot
import globalbot
def privmsg(nick,data,channel):
	for each in handlers:
		each.go(nick,data,channel)
bb=blockbot.blockbot()
tb=trekbot.trekbot()
rb=rpgbot.rpg()
handlers=[bb,tb,BBot.bbot(),mathbot.mathbot(),searchbot.searchbot(),statusbot.statusbot(),globalbot.globalbot(),rb]#Run on msg
jhandlers=[bb,tb]#Run on Join
lhandlers=[rb]#Run every loop
nhandlers=[bb]
codes=[]#wb
continuepgm=1

#irc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#irc.connect((config.network,config.port))
#q.queue.nick(config.mynick)
#q.queue.raw('USER %s %s %s :%s'%(config.mynick,config.mynick,config.mynick,config.mynick))
#print 'NICK'
#irc.send('NICK %s\r\n'%config.mynick)
#irc.send ('USER '+config.mynick+' '+config.mynick+' '+config.mynick+' :'+config.mynick+'\r\n')
needping=1

#while needping:
#	data=irc.recv(1024)
#	if data.find('PING')!=-1:
#		PONG(data)
#		time.sleep(0.2)
#		print 'IDENTIFY'
#		q.queue.send()
		#needping=0
		#print(data)

time.sleep(config.sleep_after_join)
print('STARTING LOOP')
import q
asyncore.loop()
#while continuepgm:
#	data = irc.recv (config.wait_recv)
#	print(data)
#	PONG(data)
#	if data.find('INVITE '+config.mynick+' :#')!=-1:
#		newchannel=data.split(config.mynick+' :')[-1]
#		irc.send('JOIN '+newchannel+'\r\n')
#		del newchannel
#	elif re.search(':*!*NOTICE #*:',data):
#		nick=data[1:data.find('!')]
#		channel=data[data.find(' NOTICE ')+8:data.find(':')]
#		words=data[data.find('NOTICE')+6:]
#		words=words[words.find(':'):]
#		for handler in nhandlers:
#			handler.notice(nick,channel,words)
#	elif data.find(' PRIVMSG ')!=-1:
#		channel=data.split(' PRIVMSG ')[1]
#		channel=channel.split(' :')[0]
#		nick=data.split('!')[0][1:]
#		for handler in handlers:
#			handler.go(nick,data,channel)
#		if data.find('?reload')!=-1:
#			del rb
#			handlers.pop()
#			lhandlers.pop()
#			reload(rpgbot)
#			rb=rpgbot.rpg()
#			handlers.append(rb)
#			lhandlers.append(rb)
#	elif data.find(' JOIN :#')!=-1:
#		nick=data.split('!')[0][1:]
#		if nick.find('#')==-1:
#			channel='#'+data.split(' :#')[-1][0:-2]
#			ip=data.split('@')[1].split(' JOIN')[0]
#			user=data.split('@')[0].split('!')[-1]
#			for jhandler in jhandlers:
#				jhandler.join(nick,channel,ip,user)
#	elif re.search('[0-9]+ *'+config.mynick,data):
#		code=data.split()[1]
#		for each in codes:
#			each.code(code,data)
#	if data.strip('\r\n')=='':
#		continuepgm=0
#	for handler in lhandlers:
#		handler.loop()
#	if q.queue.get_length():
#		send=q.queue.pop()
#		print(send)
#		irc.send(send+'\r\n')
#	q.queue.send()
#irc.send('QUIT :Quit: BBot Rulez\r\n')
while 1:
	pass
