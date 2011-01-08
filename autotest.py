#! /usr/bin/python
ret_val=' '
import sys,unittest
sys.path.insert(1,sys.path[0]+'/modules')
sys.path.insert(1,sys.path[0]+'/libs')
sys.path.insert(0,sys.path[0]+'/unittests')
import bbot
import modules
import config

class test_bbot(unittest.TestCase):
	def setUp(self):
		self.bbot=modules.BBot.module('127.0.0.1')
	def test_read_dict(self):
		self.assertEqual(self.bbot.read_dict(),None)
	def test_add_factoid(self):
		self.bbot.add_factoid(('abcdefg','gfedcba'),'unittester')
		self.assertEqual(self.bbot.query_dict('abcdefg'),'gfedcba')
		self.assertEqual(self.bbot.del_factoid('abcdefg'),None,'Can not delete factoid that exists')
	def test_del_factoid(self):
		self.bbot.add_factoid(('abc','abc'),'unittester')
		self.bbot.del_factoid('abc')
		self.assertEqual(self.bbot.query_dict('abc'),None,'Factoids are not being deleted')
	def test_main_module(self):
		self.assertEqual(self.bbot.privmsg('aj00200',':aj00200!aj00200@FOSSnet/staff/oper/aj00200 PRIVMSG #bots :abcdefg','#bots'),None)#Do a quick check to make sure it works

class test_api(unittest.TestCase):
	def test_getHost(self):
		self.assertEqual(api.getHost(':aj00200!aj00200@Fossnet/staff/aj00200 PRIVMSG #bots: hi'),'Fossnet/staff/aj00200','api.getHost() isn\'t returning hosts inside PRIVMSGs')
		self.assertEqual(api.getHost(':aj00200!aj00200@127.0.0.1 NOTICE #bots :Hi!'),'127.0.0.1','api.getHost() isn\'t returning hosts inside NOTICEs')
	def test_getConfigInt(self):
		self.assertEqual(str(type(api.getConfigInt('main','read-wait'))),'<type \'int\'>')
	def test_scheckIfSperUsers(self):
		self.assertEqual(api.checkIfSuperUser('123!456@lsjdlkfjslkdf.com PRIVMSG #bots :test'),False)

import api
import modules.BBot
import modules.mathbot

if __name__ == '__main__':
	unittest.main()

