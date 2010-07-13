#! /usr/bin/python
import sys
import api
import unittest
import q
import config
import socket
import thread
sys.path.insert(0,sys.path[0]+'/modules/')
import BBot
import rpgbot
import statusbot
class TestQueue(unittest.TestCase):
    def setUp(self):
        self.q=q.queue_class()
    def tearDown(self):
        del self.q
    def test_get_length(self):
        self.assertEqual(0,self.q.get_length())
        self.q.raw('stuff')
        self.q.append(('#help','hi'))
        self.assertEqual(2,self.q.get_length())
        self.assertEqual('stuff',self.q.pop())
        self.assertEqual('PRIVMSG #help :hi',self.q.pop())
        self.assertEqual(0,self.q.get_length())
class TestBBot(unittest.TestCase):
    def setUp(self):
        self.b=BBot.bbot()
    def testHi(self):
        self.b.go('aj00200',':aj002!aj00200@FOSSnet/developer/aj00200 PRIVMSG #bots :?hi','#bots')
        self.assertEqual('PRIVMSG #bots :aj00200: Hi',q.queue.pop())
        self.b.go('aj00200','aj00200!aj00200@FOSSnet/developer/aj00200 PRIVMSG #bots :?ping','#bots')
        self.assertEqual('PRIVMSG #bots :aj00200: pong',q.queue.pop(),'ping:::pong seems to be missing or incorrect in bbot/dict.  Please add it again.')
class TestStatusBot(unittest.TestCase):
    def setUp(self):
        self.s=statusbot.statusbot()
    def test_status(self):
        self.s.go('aj00200','aj00200!aj00200@FOSSnet/developer/aj00200 PRIVMSG #bots :?status Hi','#bots')
        self.s.go('aj00200','aj00200!aj00200@FOSSnet/developer/aj00200 PRIVMSG #bots :?whereis AJ00200','#bots')
        self.assertEqual(1,q.queue.get_length(),'?whereis isn\'t appending to queue')
        self.assertEqual('PRIVMSG #bots :aj00200: aj00200 is: Hi',q.queue.pop(),'All nick cases should be accepted for ?whereis')
class TestRpg(unittest.TestCase):
    def setUp(self):
        self.rpg=rpgbot.rpg()
    def test_players(self):
        self.rpg.go('aj00200',':aj00200!aj00200@FOSSnet/developer/aj00200 PRIVMSG #rpg :?players','#rpg')
        self.assertEqual('PRIVMSG #rpg :0',q.queue.pop())
    def test_loop(self):
        self.rpg.loop()
if __name__ == '__main__':
    unittest.main()

