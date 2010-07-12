#! /usr/bin/python
import sys
import unittest
import q
import config
import socket
import thread
sys.path.insert(0,sys.path[0]+'/modules/')
import BBot
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
        self.b.go('aj00200',':aj002!aj00200@FOSSnet/developer/aj00200 L PRIVMSG #bots :?hi','#bots')
        self.assertEqual('PRIVMSG #bots :aj00200: hi',q.queue.pop())
        self.b.go('aj00200','aj00200!aj00200@FOSSnet/developer/aj00200 PRIVMSG #bots :?ping','#bots')
        self.assertEqual('PRIVMSG #bots :aj00200: pong',q.queue.pop(),'ping:::pong seems to be missing or incorrect in bbot/dict.  Please add it again.')
if __name__ == '__main__':
    unittest.main()

