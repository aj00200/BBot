'''Import the necessary modules to preform unit tests on the API
and then define the class to do it with for the unittest module'''

import unittest
import api

class TestAPI(unittest.TestCase):
    '''Preform unittests on the API module'''
    # Data parsing functions
    def test_get_host(self):
        '''Test if the get_host function is working'''
        self.assertEqual(api.get_host(':a!b@host PRIVMSG #d :e'), 'host')

    def test_get_nick(self):
        '''Test if the get_nick function is working'''
        self.assertEqual(api.get_nick(':nick!b@c PRIVMSG #d :e'), 'nick')

    def test_get_ident(self):
        '''Test if the get_ident function is working'''
        self.assertEqual(api.get_ident(':a!ident@c PRIVMSG #d :e'), 'ident')

    def test_get_message(self):
        '''Test if the get_message function is working'''
        self.assertEqual(api.get_message(':a!b@c PRIVMSG #d :msg'), 'msg')

    def test_host_in_list(self):
        '''Test if the host_in_list function is working'''
        self.assertEqual(api.host_in_list(':a!b@c PRIVMSG #d :e', ['c']),
                         True, 'api.host_in_list is not functioning')

    # Command Hooks
    def test_hooks_existence(self):
        '''Ensure that the hooks variable is existent and available to
        external modules such as the backend which must use it'''
        self.assertEqual(api.hooks, {},
                         'api.hooks does not exist or contains data')

    def test_hook_server_must_exist(self):
        '''Make sure that the server the command is being hooked to is
        checked to exist before hooking the command'''
        api.hooks = {}
        api.hook_command('blah',
                         self.null_callback, 'irc.doesnotexist.com')
        self.assertEqual(api.hooks, {},
                         'Hooks are being created for nonexistant nets')

    def test_hook_command_function(self):
        '''Test to make sure that the hook_command function actually
        hooks the command to the proper server'''
        api.hooks = {'irc.pretendnetwork.example.com':{}}
        api.hook_command('blah',
                         self.null_callback, 'irc.pretendnetwork.example.com')
        self.assertEqual(api.hooks, {'irc.pretendnetwork.example.com':
                                         {'blah':self.null_callback}})

    # Misc
    def null_callback(self, a01 = None, a02 = None, a03 = None, a04 = None):
        '''A null callback for use for anything that requires a callback
        but does not need the data returned by the callback'''
        pass
