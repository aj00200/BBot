#! /usr/bin/python
ret_val=' '
import sys,unittest
sys.path.insert(1,sys.path[0]+'/modules')
sys.path.insert(1,sys.path[0]+'/libs')
sys.path.insert(0,sys.path[0]+'/unittests')
import q,bbot

class test_bbot(unittest.TestCase):
    def setUp(self):
        self.bbot=bbot('127.0.0.1')
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
        self.assertEqual(self.bbot.go('aj00200',':aj00200!aj00200@FOSSnet/staff/oper/aj00200 PRIVMSG #bots :abcdefg','#bots'),None)#Do a quick check to make sure it works
        self.assertEqual(self.bbot.go('aj00200',':aj00200!aj00200@FOSSnet/staff/oper/aj00200 PRIVMSG #bots :?hi','#bots'),None)
        self.assertEqual(self.bbot.go('aj00200',':aj00200!aj00200@FOSSnet/staff/oper/aj00200 PRIVMSG #bots :?add test:::test','#bots'),None)
        self.assertEqual(self.bbot.query_dict('test'),'test','?add Command seems broken')
        
class test_api(unittest.TestCase):
    def test_getHost(self):
        self.assertEqual(api.getHost(':aj00200!aj00200@Fossnet/staff/aj00200 PRIVMSG #bots: hi'),'Fossnet/staff/aj00200','api.getHost() isn\'t returning hosts inside PRIVMSGs')
        self.assertEqual(api.getHost(':aj00200!aj00200@127.0.0.1 NOTICE #bots :Hi!'),'127.0.0.1','api.getHost() isn\'t returning hosts inside NOTICEs')
    def test_getConfigInt(self):
        self.assertEqual(str(type(api.getConfigInt('main','read-wait'))),'<type \'int\'>')
    def test_scheckIfSperUsers(self):
        self.assertEqual(api.checkIfSuperUser('123!456@lsjdlkfjslkdf.com PRIVMSG #bots :test'),False)
        
class test_mathwiz(unittest.TestCase):
    def test_slope(self):
        self.assertEqual(str(mathwiz.slope(0,0,1,1)),'1/1')
    def test_line(self):
        self.assertEqual(str(mathwiz.line(0,0,19,7)),'<line slope=7/19;>')
    def test_triangle(self):
        t=mathwiz.triangle(0,0,2,2,5,5)
        self.assertEqual(t.sides['ab'],2.8284271247461903)
        self.assertEqual(t.sides['bc'],4.2426406871192848)
        self.assertEqual(t.sides['ca'],7.0710678118654755)
        self.assertEqual(t.type,'Scalene','Triangle identification broken')
from BBot import bbot
import api,mathbot,mathwiz

if __name__ == '__main__':
    unittest.main()

