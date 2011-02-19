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
    # Command Hooks
    def test_hooks_existence(self):
        self.assertEqual(api.hooks,{})
    def test_hook_server_must_exist(self):
        api.hooks={}
        api.hook_command('blah',self.null_callback,'irc.fakenetwork.example.com')
        self.assertEqual(api.hooks,{})
    def test_hook_command_function(self):
        api.hooks={'irc.pretendnetwork.example.com':{}}
        api.hook_command('blah',self.null_callback,'irc.pretendnetwork.example.com')
        self.assertEqual(api.hooks,{'irc.pretendnetwork.example.com':{'blah':self.null_callback}})
    # Misc
    def null_callback(a1=None,a2=None,a3=None,a4=None,a5=None,a6=None):
        pass
