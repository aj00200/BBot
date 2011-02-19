'''This provides a two-way bridge between two channels on different networks.'''

import api
class Module(api.module):
    commands = []
    chan1 = '#bbot' # Channel on net1
    chan2 = '#bbot' # Channel on net2
    net1 = 'irc.fossnet.info'
    net2 = 'irc.freenode.net'
    def __init__(self, server):
        self.
        api.module.__init__(self, server)
    def privmsg(self, nick, data, channel):
        if channel == self.chan1 and self.__server__ == self.net1:
            self.to = self.net2
        elif channel == self.chan2 and self.__server__ == self.net2:
            self.to = self.net1
        else:
            self.to = self.net1
        try:
            q.append(self.to, (channel, '<%s> %s'%(nick, data[data.find(' :')+2:])))
        except Exception:
            pass
