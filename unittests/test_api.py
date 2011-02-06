import unittest
import api
class TestAPI(unittest.TestCase):
    # Data parsing functions
    def test_getHost(self):
        self.assertEqual(api.getHost(':a!b@host PRIVMSG #d :e'),'host')
    def test_getNick(self):
        self.assertEqual(api.getNick(':nick!b@c PRIVMSG #d :e'),'nick')
    def test_getIdent(self):
        self.assertEqual(api.getIdent(':a!ident@c PRIVMSG #d :e'),'ident')
    def test_getMessage(self):
        self.assertEqual(api.getMessage(':a!b@c PRIVMSG #d :msg'),'msg')
    def test_hostInList(self):
        self.assertEqual(api.hostInList(':a!b@c PRIVMSG #d :e',['c']),True)
