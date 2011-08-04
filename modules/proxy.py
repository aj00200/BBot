'''This provides a two-way bridge between two channels which are on different
IRC networks by sending messages between them'''

import api
class Module(api.Module):
    commands = []
    chan1 = '#bbot' # Channel on net1
    chan2 = '#bbot' # Channel on net2
    net1 = 'irc.fossnet.info'
    net2 = 'irc.freenode.net'

    def privmsg(self, nick, data, channel):
        if channel == self.chan1 and self.__address__ == self.net1:
            self.to = self.net2
        elif channel == self.chan2 and self.__address__ == self.net2:
            self.to = self.net1
        else:
            self.to = self.net1
        try:
            api.backend.connections[self.to].push('PRIVMSG %s :<%s> %s\r\n' %
                                       (channel, nick, api.get_message(data)))
        except Exception:
            pass
