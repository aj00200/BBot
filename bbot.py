#! /usr/bin/python
import q
#this bot is licensed under the GNU GPL v3.0
#http://www.gnu.org/licenses/gpl.html
version='2.5'
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

bb=blockbot.blockbot()
tb=trekbot.trekbot()
rb=rpgbot.rpg()
handlers=[bb,tb,BBot.bbot(),mathbot.mathbot(),searchbot.searchbot(),statusbot.statusbot(),globalbot.globalbot(),rb]#Run on msg
jhandlers=[bb,tb]#Run on Join
lhandlers=[]#Run every loop
nhandlers=[bb]
codes=[]#wb
continuepgm=1
#needping=1


time.sleep(config.sleep_after_join)
print('STARTING LOOP')
import q
asyncore.loop()

while 1:
	pass
