import unittest
import api
class TestAPI(unittest.TestCase):
    # Data parsing functions
    def test_get_host(self):
        self.assertEqual(api.get_host(':a!b@host PRIVMSG #d :e'),'host')
    def test_get_nick(self):
        self.assertEqual(api.get_nick(':nick!b@c PRIVMSG #d :e'),'nick')
    def test_get_ident(self):
        self.assertEqual(api.get_ident(':a!ident@c PRIVMSG #d :e'),'ident')
    def test_get_message(self):
        self.assertEqual(api.get_message(':a!b@c PRIVMSG #d :msg'),'msg')
    def test_host_in_list(self):
        self.assertEqual(api.host_in_list(':a!b@c PRIVMSG #d :e',['c']),True)
