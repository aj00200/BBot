#! /usr/bin/python
import q
#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='3.0'
#Scan for open proxies on join? 1=yes,0=no. Requires nmap and python-namp: http://nmap.org  http://xael.org/norman/python/python-nmap/

import config

#import socket
import sys
import re
import time
import colorz
import api#BBot API Functions
import asyncore
sys.path.insert(0,'%s/modules'%sys.path[0])
import BBot
import proxy
import mathbot
import searchbot
import trekbot
import blockbot
import statusbot
import globalbot
import debatebot

bb=blockbot.module(config.network)
tb=trekbot.module(config.network)
handlers=[bb,tb,BBot.module(config.network),proxy.module(config.network),mathbot.module(config.network),debatebot.module(config.network),searchbot.module(config.network),statusbot.module(config.network),globalbot.module(config.network)]#Run on msg
networks={config.network: handlers}
def add_network(name):
	print colorz.encode('Adding Network "%s"'%name,'yellow')
	networks[name]=[BBot.module(name)]
def load_module(name,server):
	print colorz.encode('Loading module "%s" for server "%s"'%(name,server),'yellow')
	try:
		networks[server].append(eval(name+'.module("%s")'%server))
	except Exception,e:
		q.append('irc.fossnet.info',(('#spam','BBot has crashed with error: %s; and args: %s'%(type(e),e.args)))) 
jhandlers=[bb,tb]#Run on Join
lhandlers=[]#Run every loop
nhandlers=[bb]
codes=[]#wb
continuepgm=1
#needping=1

#<<<<<<< HEAD:bbot.py

##time.sleep(config.sleep_after_join) # ...
if __name__ == '__main__':
	import q
	while 1:
#=======
#time.sleep(config.sleep_after_join) # ...
#if __name__ == '__main__':
#	import q
#	
#	print('STARTING LOOP')
#	while 1:
#		q.connection(config.network)
##>>>>>>> dev:bbot.py
		asyncore.loop()
