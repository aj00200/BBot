'''This module allows users to set a status that others can query.'''

import api


class Module(api.Module):
    def __init__(self, server):
        super(Module, self).__init__(server)
        self.statuses = {}

        # Hook commands
        api.hook_command('status', self.status, server)
        api.hook_command('whereis', self.whereis, server)

    def status(self, nick, channel, param=None):
        '''Set your status for other people to see'''
        nick = nick.lower()
        if param:
            self.statuses[nick] = param
            self.msg(channel, '%s: your status is set.' % nick)
        elif nick in self.statuses:
            del self.statuses[nick]
            self.msg(channel, '%s: status cleared.' % nick)

    def whereis(self, nick, channel, param=None):
        '''Check the status of someone; Parameters: None'''
        param = param.lower()
        if param and ' ' in param:
            param = param.strip()
        if param in self.statuses:
            self.msg(channel, '%s: %s left the status: %s' %
                     (nick, param, self.statuses[param]))
        elif not param:
            self.msg(channel, '%s: who\'s status do you want?' % nick)
        else:
            self.msg(channel, '%s: that person has not left a status.' % nick)
