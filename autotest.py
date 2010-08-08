#! /usr/bin/python
import sys
import unittest
sys.path.insert(1,sys.path[0]+'/modules')
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
        self.assertEqual(self.bbot.query_dict('abc'),None)
    def test_io(self):
        self.bbot.add_factoid(('hi','Hi!'))
        self.bbot.write_dict()
        self.bbot.del_factoid('hi')
        self.bbot.read_dict()
        self.assertEqual(self.bbot.query_dict('hi'),'Hi!')
from BBot import bbot
if __name__ == '__main__':
    print '==Starting Tests=='
    unittest.main()

