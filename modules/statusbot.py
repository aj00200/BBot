'''This module allows users to set a status that others can query.'''

import api
import config

class Module(api.module):
    def __init__(self, server):
        self.statuses = {}
        api.module.__init__(self, server)

        # Hook commands
        api.hook_command('status', self.status, server)
        api.hook_command('whereis', self.whereis, server)

    def status(self, nick, channel, param = None):
        '''Set your status for other people to see'''
        self.statuses[nick.lower()] = param

    def whereis(self, nick, channel, param = None):
        '''Check the status of someone; Parameters: None'''
        if param in self.statuses:
            self.msg(channel, '%s: %s left the status: %s' % (nick, param, self.statuses[param]))
        elif not param:
            self.msg(channel, '%s: who\'s status do you want?' % nick)
        else:
            self.msg(channel, '%s: that person has not left a status.' % nick)
