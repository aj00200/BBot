#! /usr/bin/python
#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='5.0 beta 0'
import q
import config
#import socket
import sys
import re
import time
import thread
import colorz
import api#BBot API Functions
import asyncore
sys.path.insert(1,'%s/libs'%sys.path[0])
sys.path.insert(0,'%s/modules'%sys.path[0])
import BBot
import proxy
import mathbot
import trekbot
import blockbot
import statusbot
import globalbot
import debatebot
networks={config.network: [blockbot.module(config.network),trekbot.module(config.network),BBot.module(config.network),proxy.module(config.network),mathbot.module(config.network),debatebot.module(config.network),statusbot.module(config.network),globalbot.module(config.network)]}
def add_network(name):
	print colorz.encode('Adding Network "%s"'%name,'yellow')
	networks[name]=[BBot.module(name)]
def load_module(name,server):
	print colorz.encode('Loading module "%s" for server "%s"'%(name,server),'yellow')
	try:
		__import__(name)
		networks[server].append(__import__(name).module(server))
	except Exception,e:
		q.append(config.network,((config.error_chan,'BBot has crashed with error: %s; and args: %s'%(type(e),e.args)))) 
def reload_module(name,server):
	try:
		for each in networks[server]:
			if isinstance(each,eval(name+'.module')):
				networks[server].pop(networks[server].index(each))
		reload(eval(name))
		networks[server].append(eval(name+'.module("%s")'%config.network))
	except Exception,e:
		q.append(config.network,((config.error_chan,'BBot has crashed with error: %s; args %s; in bbot.py'%(type(e),e.args))))
continuepgm=1
lastloop=time.time()-10
def loop():
	'''
	Calls the loop() method of each module every 5 seconds + execution time
	'''
	try:
		time.sleep(5)
		for network in networks:
			for module in networks[network]:
				module.loop()
	except Exception,e:
		q.append(config.network,((config.error_chan,'BBot has crashed with error: %s; args %s'%(type(e),e.args))))
if __name__ == '__main__':
	thread.start_new_thread(loop,())
	import q
	asyncore.loop()
