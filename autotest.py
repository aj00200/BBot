#! /usr/bin/python
ret_val=' '
import sys
import unittest
sys.path.insert(1,sys.path[0]+'/modules')
sys.path.insert(1,sys.path[0]+'/libs')
sys.path.insert(0,sys.path[0]+'/unittests')
import q
import bbot

class test_bbot(unittest.TestCase):
    def setUp(self):
        self.bbot=bbot('127.0.0.1')
    def test_read_dict(self):
        self.assertEqual(self.bbot.read_dict(),None)
    def test_add_factoid(self):
        self.bbot.add_factoid(('abcdefg','gfedcba'))
        self.assertEqual(self.bbot.query_dict('abcdefg'),'gfedcba')
    def test_del_factoid(self):
        self.bbot.add_factoid(('abc','abc'))
        self.bbot.del_factoid('abc')
        self.assertEqual(self.bbot.query_dict('abc'),None,'Factoids are not being deleted')
    def test_io(self):
        self.bbot.add_factoid(('hi','Hi!'))
        self.bbot.write_dict()
        self.bbot.read_dict()
        self.assertEqual(self.bbot.query_dict('hi'),'Hi!','Error with reading or writing factoids')
        self.bbot.del_factoid('hi')
        self.bbot.read_dict()
        self.assertEqual(self.bbot.query_dict('hi'),'Hi!')
    def test_main_module(self):
        self.assertEqual(self.bbot.go('aj00200',':aj00200!aj00200@FOSSnet/staff/oper/aj00200 PRIVMSG #bots :abcdefg','#bots'),None)#Do a quick check to make sure it works
        self.assertEqual(self.bbot.go('aj00200',':aj00200!aj00200@FOSSnet/staff/oper/aj00200 PRIVMSG #bots :?hi','#bots'),0)
        self.assertEqual(self.bbot.go('aj00200',':aj00200!aj00200@FOSSnet/staff/oper/aj00200 PRIVMSG #bots :?add test:::test','#bots'),0)
        self.assertEqual(self.bbot.query_dict('test'),'test','?add Command seems broken')
class test_api(unittest.TestCase):
    def test_getHost(self):
        self.assertEqual(api.getHost(':aj00200!aj00200@Fossnet/staff/aj00200 PRIVMSG #bots: hi'),'Fossnet/staff/aj00200','api.getHost() isn\'t returning hosts inside PRIVMSGs')
        self.assertEqual(api.getHost(':aj00200!aj00200@127.0.0.1 NOTICE #bots :Hi!'),'127.0.0.1','api.getHost() isn\'t returning hosts inside NOTICEs')
class test_mathwiz(unittest.TestCase):
    def test_slope(self):
        self.assertEqual(str(mathwiz.slope(0,0,1,1)),'1/1')
from BBot import bbot
import api
import mathbot
import mathwiz
if __name__ == '__main__':
    unittest.main()

